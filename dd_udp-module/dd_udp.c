#include <linux/module.h>          // Provides macros and functions for kernel module development
#include <linux/kernel.h>          // Enables kernel logging functions like printk
#include <linux/netfilter.h>       // Core Netfilter framework for packet filtering
#include <linux/netfilter_ipv4.h>  // IPv4-specific Netfilter hooks and definitions
#include <linux/skbuff.h>          // Socket buffer (sk_buff) handling for network packets
#include <linux/ip.h>              // IP header structure and utilities
#include <linux/udp.h>             // UDP header structure and protocol definitions
#include <net/net_namespace.h>     // Network namespace management for isolation
#include <net/netlink.h>           // Netlink socket for kernel-user space communication
#include <linux/delay.h>           // Delay functions like msleep (not used here but included)
#include <linux/jiffies.h>         // Kernel timing utilities (jiffies counter)
#include <linux/atomic.h>          // Atomic operations for thread-safe counters
#include <net/checksum.h>          // For checksum functions like csum_partial and csum_tcpudp_nofold

MODULE_AUTHOR("G.J. den Besten");
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Enhanced UDP Data Diode Module with Packet/Datagram Loss, "
                   "Corruption Tracking, and Offloading Awareness. "
                   "This code forms an integral part of my Masters graduation project.");

#define NETLINK_DIODE 31         // Custom Netlink protocol number (unique identifier)
#define NL_GROUP 1               // Netlink multicast group for broadcasting messages

// Netlink command definitions for user-space interaction
#define NL_CMD_RESET_COUNTERS 1  // Command to reset datagram counters
#define NL_CMD_QUERY_COUNTERS 2  // Command to query current datagram counts
#define NL_CMD_QUERY_CONFIG 3    // Command to query module configuration
#define NL_CMD_TOGGLE_VERBOSE 4  // Command to toggle verbose logging mode
#define NL_CMD_SET_CHECKSUM 5    // Command to enable UDP checksum verification
#define NL_CMD_UNSET_CHECKSUM 6  // Command to disable UDP checksum verification

// Module parameters configurable at load time via insmod
static int sender_ns_fd = -1;           // File descriptor for sender network namespace
static int receiver_ns_fd = -1;         // File descriptor for receiver network namespace
static int verbose_netlink = 0;         // Toggle verbose logging (0 = off, 1 = on)
static int send_init_msg = 1;           // Send initialization message on load (0 = off, 1 = on)
static char *sender_ifname = "eth0";    // Default sender interface name
static char *receiver_ifname = "eth1";  // Default receiver interface name

// Register module parameters with permissions (0644 = readable/writable by root, readable by others)
module_param(sender_ns_fd, int, 0644);      // Sender namespace FD as integer
module_param(receiver_ns_fd, int, 0644);    // Receiver namespace FD as integer
module_param(verbose_netlink, int, 0644);   // Verbose logging toggle as integer
module_param(send_init_msg, int, 0644);     // Init message toggle as integer
module_param(sender_ifname, charp, 0644);   // Sender interface name as string
module_param(receiver_ifname, charp, 0644); // Receiver interface name as string

// Parameter descriptions visible via modinfo
MODULE_PARM_DESC(sender_ns_fd, "Sender namespace file descriptor");
MODULE_PARM_DESC(receiver_ns_fd, "Receiver namespace file descriptor");
MODULE_PARM_DESC(verbose_netlink, "Enable verbose logging (0 = off, 1 = on)");
MODULE_PARM_DESC(send_init_msg, "Send module loaded message on init (0 = off, 1 = on)");
MODULE_PARM_DESC(sender_ifname, "Sender interface name");
MODULE_PARM_DESC(receiver_ifname, "Receiver interface name");

// Global variables for module state
static struct net *sender_netns = NULL;                   // Pointer to sender network namespace
static struct sock *nl_sk = NULL;                         // Netlink socket for user-space communication
static struct net *receiver_netns = NULL;                 // Pointer to receiver network namespace
static atomic64_t sent_datagrams = ATOMIC64_INIT(0);      // Atomic counter for sent UDP datagrams
static atomic64_t received_datagrams = ATOMIC64_INIT(0);  // Atomic counter for received UDP datagrams
static atomic64_t corrupted_datagrams = ATOMIC64_INIT(0); // Atomic counter for corrupted UDP datagrams
static int enable_checksum = 0;                           // Toggle for UDP checksum verification (1 = enabled, 0 = disabled)

/**
 * nl_send - Send a message to user-space via Netlink
 * @message: The message string to send
 * @pid: Process ID of the recipient (0 for broadcast to group)
 *
 * Allocates a socket buffer, constructs a Netlink message, and sends it to user-space.
 */
static void nl_send(const char *message, pid_t pid)
{
    struct sk_buff *skb;                   // Socket buffer to hold the Netlink message
    struct nlmsghdr *nlh;                  // Netlink message header
    size_t msg_len = strlen(message) + 1;  // Message length including null terminator

    // Allocate memory for the Netlink message
    skb = nlmsg_new(msg_len, GFP_KERNEL);  // Allocate memory for the Netlink message
    if (!skb) {
        printk(KERN_ERR "dd_udp: Failed to allocate skb\n");
        return;
    }

    // Construct the Netlink message in the socket buffer
    nlh = nlmsg_put(skb, 0, 0, NLMSG_DONE, msg_len, 0);  // Construct the message
    if (!nlh) {
        kfree_skb(skb);  // Free buffer if construction fails
        return;
    }
    strcpy(nlmsg_data(nlh), message);     // Copy message into payload
    netlink_unicast(nl_sk, skb, pid, 0);  // Send message (blocking) (0 = no flags)
}

/**
 * nl_input - Handle incoming Netlink messages from user-space
 * @skb: Socket buffer containing the incoming message
 *
 * Processes commands from user-space to manage counters or toggle settings.
 */
static void nl_input(struct sk_buff *skb)
{
    struct nlmsghdr *nlh = nlmsg_hdr(skb);  // Extract Netlink message header
    pid_t pid = nlh->nlmsg_pid;             // Get sender's process ID
    char msg[128];                          // Buffer for response messages

    // Process the command based on message type
    switch (nlh->nlmsg_type) {
        case NL_CMD_RESET_COUNTERS:  // Reset all datagrams counters
            atomic64_set(&sent_datagrams, 0);
            atomic64_set(&received_datagrams, 0);
            atomic64_set(&corrupted_datagrams, 0);
            break;
        case NL_CMD_QUERY_COUNTERS:  // Report current datagrams counts
            snprintf(msg, sizeof(msg), "Sent: %llu, Received: %llu, Corrupted: %llu",
                     atomic64_read(&sent_datagrams), atomic64_read(&received_datagrams),
                     atomic64_read(&corrupted_datagrams));
            nl_send(msg, pid);
            break;
        case NL_CMD_QUERY_CONFIG:  // Send current configuration details
            snprintf(msg, sizeof(msg), "Sender IF: %s (ns_fd: %d), Receiver IF: %s (ns_fd: %d), Verbose: %d, Checksumming: %d", 
                     sender_ifname, sender_ns_fd,  receiver_ifname, receiver_ns_fd, verbose_netlink, enable_checksum);
            nl_send(msg, pid);
            break;
        case NL_CMD_TOGGLE_VERBOSE:  // Toggle verbose logging
            verbose_netlink = !verbose_netlink;
            break;
        case NL_CMD_SET_CHECKSUM:  // Enable UDP checksum verification
            enable_checksum = 1;
            break;
        case NL_CMD_UNSET_CHECKSUM:  // Disable UDP checksum verification
            enable_checksum = 0;
            break;
    }
}

/**
 * sender_hook - Netfilter hook for outgoing datagrams in sender namespace
 * @priv: Private data (unused)
 * @skb: Socket buffer with the datagrams
 * @state: Netfilter hook state
 *
 * Filters outgoing UDP datagrams on the sender interface, adding checksums only if not offloaded.
 */
static unsigned int sender_hook(void *priv, struct sk_buff *skb, const struct nf_hook_state *state)
{
    struct iphdr *iph;   // Pointer to IP header
    struct udphdr *udph; // Pointer to UDP header
    char msg[128];       // Buffer for Netlink messages

    // Skip datagrams not from sender interface or invalid packets
    if (!skb || strcmp(state->out->name, sender_ifname) != 0) {
        return NF_ACCEPT;  // Pass non-matching datagrams
    }

    // Extract IP header
    iph = ip_hdr(skb);
    if (!iph || iph->protocol != IPPROTO_UDP) {
        if (verbose_netlink) {
            snprintf(msg, sizeof(msg), "Dropped non-UDP datagrams on %s", sender_ifname);
            nl_send(msg, 0);  // Notify user-space
        }
        return NF_DROP;  // Drop non-UDP datagrams
    }

    // Extract UDP header
    udph = udp_hdr(skb);
    if (!udph) {
        return NF_DROP;  // Drop if UDP header is missing
    }

    // Compute checksum only if enabled, not already set, and not offloaded by NIC
    if (enable_checksum && udph->check == 0 && skb->ip_summed != CHECKSUM_PARTIAL) {
        unsigned short udp_len = ntohs(udph->len);  // UDP length in host byte order
        unsigned int csum = csum_tcpudp_nofold(iph->saddr, iph->daddr, udp_len, IPPROTO_UDP, 0);  // Pseudo-header checksum
        csum = csum_partial(udph, udp_len, csum);  // Include UDP header and data
        udph->check = csum_fold(csum);  // Final 16-bit checksum
    } else if (skb->ip_summed == CHECKSUM_PARTIAL) {
        if (verbose_netlink) {
            snprintf(msg, sizeof(msg), "Checksum offloaded to NIC for UDP on %s", sender_ifname);
            nl_send(msg, 0);  // Log offloading if verbose
        }
    }

    // Increment sent datagrams counter
    atomic64_inc(&sent_datagrams);
    if (verbose_netlink) {
        snprintf(msg, sizeof(msg), "Accepted UDP from %pI4 to %pI4 on %s",
                 &iph->saddr, &iph->daddr, sender_ifname);
        nl_send(msg, 0);  // Log datagrams acceptance
    }
    return NF_ACCEPT;  // Allow datagrams to proceed
}

/**
 * receiver_hook - Netfilter hook for incoming datagrams in receiver namespace
 * @priv: Private data (unused)
 * @skb: Socket buffer with the datagrams
 * @state: Netfilter hook state
 *
 * Filters incoming UDP datagrams, verifying checksums unless offloaded by NIC.
 */
static unsigned int receiver_hook(void *priv, struct sk_buff *skb, const struct nf_hook_state *state)
{
    struct iphdr *iph;      // Pointer to IP header
    struct udphdr *udph;    // Pointer to UDP header
    char msg[128];          // Buffer for Netlink messages to user-space

    // Skip datagrams that are invalid or not destined for the receiver interface
    if (!skb || strcmp(state->in->name, receiver_ifname) != 0) {
        return NF_ACCEPT;  // Pass non-matching datagrams unchanged
    }

    // Extract the IP header from the socket buffer
    iph = ip_hdr(skb);
    if (!iph || iph->protocol != IPPROTO_UDP) {
        // Drop non-UDP datagrams and log if verbose mode is enabled
        if (verbose_netlink) {
            snprintf(msg, sizeof(msg), "Dropped non-UDP datagrams on %s", receiver_ifname);
            nl_send(msg, 0);  // Send notification to user-space via Netlink
        }
        return NF_DROP;  // Drop the datagram if it’s not UDP
    }

    // Extract the UDP header based on the IP header length (ihl is in 4-byte units)
    udph = (struct udphdr *)((char *)iph + (iph->ihl * 4));
    if (!udph) {
        return NF_DROP;  // Drop the datagram if the UDP header is missing or inaccessible
    }

    // Verify checksum if enabled and the datagram includes a checksum (non-zero)
    int datagram_counted = 0;
    if (enable_checksum && udph->check != 0) {
        if (skb->ip_summed == CHECKSUM_UNNECESSARY) {
            datagram_counted = 1;
            // NIC has already verified the checksum; trust the hardware
            if (verbose_netlink) {
                snprintf(msg, sizeof(msg), "Checksum verified by NIC for UDP on %s", receiver_ifname);
                nl_send(msg, 0);  // Log NIC verification
            }
        } else if (skb->ip_summed == CHECKSUM_COMPLETE) {
            // NIC computed the checksum; check if it indicates corruption
            if (skb->csum != 0) {
                atomic64_inc(&corrupted_datagrams);  // Increment counter for corrupted datagrams
                if (verbose_netlink) {
                    snprintf(msg, sizeof(msg), "Corrupted UDP datagram (NIC computed, csum=%u)", skb->csum);
                    nl_send(msg, 0);  // Log corruption detected by NIC
                } 
            } else {  // NIC computed, valid
                datagram_counted = 1;
            }
        } else {
            // No NIC offloading; manually compute and verify the checksum
            // Check if the skb is non-linear (data is fragmented across multiple buffers)
            if (skb_is_nonlinear(skb)) {
                // Linearize the skb to make data contiguous for checksum computation
                if (skb_linearize(skb) < 0) {
                    return NF_DROP;  // Drop the datagram if linearization fails
                }
                // Recalculate header pointers after linearization, as memory layout has changed
                iph = ip_hdr(skb);
                udph = (struct udphdr *)((char *)iph + (iph->ihl * 4));
            }

            unsigned short udp_len = ntohs(udph->len);   // Get UDP length in host byte order for checksum computation

            // Compute the checksum manually
            // Step 1: Compute pseudo-header checksum (source/dest IPs, protocol, UDP length)
            unsigned int csum = csum_tcpudp_nofold(iph->saddr, iph->daddr, udp_len, IPPROTO_UDP, 0);
            // Step 2: Include UDP header and payload in the checksum
            csum = csum_partial(udph, udp_len, csum);
            // Step 3: Fold the 32-bit checksum into 16 bits
            unsigned short computed_csum = csum_fold(csum);

            // Verify checksum: it should be 0 if valid
            if (computed_csum != 0) {
                atomic64_inc(&corrupted_datagrams);  // Increment counter for corrupted datagrams
                if (verbose_netlink) {
                    snprintf(msg, sizeof(msg), "Corrupted UDP datagram: computed_csum=0x%04x != 0", computed_csum);
                    nl_send(msg, 0);  // Log checksum failure
                }
            } else {
                datagram_counted = 1;
            }
        }
    } else {
        datagram_counted = 1;
    }

    if (datagram_counted) {
        // Increment the received datagram counter
        atomic64_inc(&received_datagrams);
        if (verbose_netlink) {
            // Log successful datagram reception with source and destination IPs
            snprintf(msg, sizeof(msg), "Received UDP from %pI4 to %pI4 on %s",
                     &iph->saddr, &iph->daddr, receiver_ifname);
            nl_send(msg, 0);  // Send log to user-space
        }
    }
    return NF_ACCEPT;  // Allow the datagram to proceed through the network stack
}

// Netfilter hook configurations
static struct nf_hook_ops sender_ops = {
    .hook     = sender_hook,       // Sender hook function
    .pf       = NFPROTO_IPV4,      // IPv4 protocol family
    .hooknum  = NF_INET_LOCAL_OUT, // Hook for outgoing packets
    .priority = NF_IP_PRI_FIRST    // Highest priority
};

static struct nf_hook_ops receiver_ops = {
    .hook     = receiver_hook,     // Receiver hook function
    .pf       = NFPROTO_IPV4,      // IPv4 protocol family
    .hooknum  = NF_INET_LOCAL_IN,  // Hook for incoming packets
    .priority = NF_IP_PRI_FIRST    // Highest priority
};

/**
 * diode_init - Module initialization function
 */
static int __init diode_init(void)
{
    int ret;
    struct netlink_kernel_cfg cfg = {
        .input = nl_input,   // Netlink input handler
        .groups = NL_GROUP,  // Multicast group support
    };
    struct net_device *dev;  // For interface validation

    // Create Netlink socket for kernel-user space communication
    nl_sk = netlink_kernel_create(&init_net, NETLINK_DIODE, &cfg);
    if (!nl_sk) {
        printk(KERN_ERR "dd_udp: Failed to create Netlink socket\n");
        return -ENOMEM;  // Memory allocation error
    }

    // Check if namespace file descriptors are provided
    if (sender_ns_fd < 0 || receiver_ns_fd < 0) {
        printk(KERN_ERR "dd_udp: Missing namespace FDs\n");
        netlink_kernel_release(nl_sk);
        return -EINVAL;  // Invalid argument error
    }

    // Retrieve sender network namespace from file descriptor
    sender_netns = get_net_ns_by_fd(sender_ns_fd);
    if (IS_ERR(sender_netns)) {
        printk(KERN_ERR "dd_udp: Invalid sender FD: %ld\n", PTR_ERR(sender_netns));
        netlink_kernel_release(nl_sk);
        return PTR_ERR(sender_netns);  // Return error code
    }

    // Retrieve receiver network namespace from file descriptor
    receiver_netns = get_net_ns_by_fd(receiver_ns_fd);
    if (IS_ERR(receiver_netns)) {
        printk(KERN_ERR "dd_udp: Invalid receiver FD: %ld\n", PTR_ERR(receiver_netns));
        put_net(sender_netns);
        netlink_kernel_release(nl_sk);
        return PTR_ERR(receiver_netns); // Return error code
    }

    // Validate sender interface exists in its namespace
    dev = dev_get_by_name(sender_netns, sender_ifname);
    if (!dev) {
        printk(KERN_ERR "dd_udp: Sender interface %s not found\n", sender_ifname);
        put_net(sender_netns);
        put_net(receiver_netns);
        netlink_kernel_release(nl_sk);
        return -ENODEV;  // No such device error
    }
    dev_put(dev);  // Release device reference

     // Validate receiver interface exists in its namespace
    dev = dev_get_by_name(receiver_netns, receiver_ifname);
    if (!dev) {
        printk(KERN_ERR "dd_udp: Receiver interface %s not found\n", receiver_ifname);
        put_net(sender_netns);
        put_net(receiver_netns);
        netlink_kernel_release(nl_sk);
        return -ENODEV;  // No such device error
    }
    dev_put(dev);  // Release device reference

    // Register sender hook in sender namespace
    ret = nf_register_net_hook(sender_netns, &sender_ops);
    if (ret) {
        printk(KERN_ERR "dd_udp: Failed to register sender hook\n");
        put_net(sender_netns);
        put_net(receiver_netns);
        netlink_kernel_release(nl_sk);
        return ret;  // Return registration error
    } else {
        printk(KERN_INFO "dd_udp: Registered sender hook for sender FD %d, sender_if %s\n",
            sender_ns_fd, sender_ifname);
    }

    // Register receiver hook in receiver namespace
    ret = nf_register_net_hook(receiver_netns, &receiver_ops);
    if (ret) {
        printk(KERN_ERR "dd_udp: Failed to register receiver hook\n");
        nf_unregister_net_hook(sender_netns, &sender_ops);  // Cleanup sender hook
        put_net(sender_netns);
        put_net(receiver_netns);
        netlink_kernel_release(nl_sk);
        return ret;  // Return registration error
    } else {
        printk(KERN_INFO "dd_udp: Registered receiver hook for receiver FD %d, receiver_if %s\n",
            receiver_ns_fd, receiver_ifname);
    }

    // Log successful module initialization
    printk(KERN_INFO "dd_udp: Loaded with sender FD %d -> receiver FD %d, sender_if %s, receiver_if %s\n",
           sender_ns_fd, receiver_ns_fd, sender_ifname, receiver_ifname);
    if (send_init_msg) {
        nl_send("dd_udp: Module loaded", 0);  // Broadcast to group
    }
    return 0;
}

/**
 * diode_exit - Module cleanup function
 */
static void __exit diode_exit(void)
{
    nf_unregister_net_hook(receiver_netns, &receiver_ops); // Remove receiver input hook
    nf_unregister_net_hook(sender_netns, &sender_ops);     // Remove sender output hook
    if (sender_netns) put_net(sender_netns);               // Free sender namespace
    if (receiver_netns) put_net(receiver_netns);           // Free receiver namespace
    if (nl_sk) netlink_kernel_release(nl_sk);              // Free Netlink socket
    printk(KERN_INFO "dd_udp: Module unloaded\n");
}

module_init(diode_init);  // Called on module load
module_exit(diode_exit);  // Called on module unload
