#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <string.h>

void print_help(const char *prog_name) {
    printf("Usage: %s [-h] [-n] [-v] <sender_ns> <receiver_ns> [sender_ifname] [receiver_ifname]\n", prog_name);
    printf("\n");
    printf("Loads the dd_udp kernel module with specified namespaces and interfaces.\n");
    printf("\n");
    printf("Options and Arguments:\n");
    printf("  -h              Display this help message and exit.\n");
    printf("  -n              Disable sending the initial 'module loaded' Netlink message.\n");
    printf("  -v              Enable verbose Netlink messaging for accepted/received UDP packets.\n");
    printf("  sender_ns       Name of the sender namespace (e.g., sender_ns).\n");
    printf("  receiver_ns     Name of the receiver namespace (e.g., receiver_ns).\n");
    printf("  sender_ifname   (Optional) Sender interface name (e.g., enp1s0). Default: eth0\n");
    printf("  receiver_ifname (Optional) Receiver interface name (e.g., enp6s0). Default: eth1\n");
    printf("\n");
    printf("Examples:\n");
    printf("  %s sender_ns receiver_ns\n", prog_name);
    printf("  %s -n sender_ns receiver_ns enp1s0 enp6s0\n", prog_name);
    printf("  %s -n -v sender_ns receiver_ns enp1s0 enp6s0\n", prog_name);
}

int main(int argc, char *argv[]) {
    int sender_fd, receiver_fd;
    char params[256];
    const char *sender_ns = NULL;
    const char *receiver_ns = NULL;
    const char *sender_if = "eth0";
    const char *receiver_if = "eth1";
    int send_init = 1;
    int verbose = 0;
    int arg_offset = 1;

    for (int i = 1; i < argc && argv[i][0] == '-'; i++) {
        if (strcmp(argv[i], "-h") == 0 || strcmp(argv[i], "--help") == 0) {
            print_help(argv[0]);
            return 0;
        } else if (strcmp(argv[i], "-n") == 0) {
            send_init = 0;
            arg_offset++;
        } else if (strcmp(argv[i], "-v") == 0) {
            verbose = 1;
            arg_offset++;
        } else {
            fprintf(stderr, "Unknown option: %s\n", argv[i]);
            print_help(argv[0]);
            return 1;
        }
    }

    if (argc < arg_offset + 2) {  // Need at least sender_ns and receiver_ns
        fprintf(stderr, "Error: Missing namespace arguments.\n");
        print_help(argv[0]);
        return 1;
    }

    sender_ns = argv[arg_offset];
    receiver_ns = argv[arg_offset + 1];
    arg_offset += 2;

    if (argc > arg_offset) {
        sender_if = argv[arg_offset];
        arg_offset++;
    }
    if (argc > arg_offset) {
        receiver_if = argv[arg_offset];
        arg_offset++;
    }
    if (argc > arg_offset + 1) {
        fprintf(stderr, "Error: Too many arguments.\n");
        print_help(argv[0]);
        return 1;
    }

    // Open sender namespace FD
    char sender_path[256];
    snprintf(sender_path, sizeof(sender_path), "/var/run/netns/%s", sender_ns);
    sender_fd = open(sender_path, O_RDONLY);
    if (sender_fd < 0) {
        perror("Failed to open sender namespace");
        return 1;
    }

    // Open receiver namespace FD
    char receiver_path[256];
    snprintf(receiver_path, sizeof(receiver_path), "/var/run/netns/%s", receiver_ns);
    receiver_fd = open(receiver_path, O_RDONLY);
    if (receiver_fd < 0) {
        perror("Failed to open receiver namespace");
        close(sender_fd);
        return 1;
    }

    snprintf(params, sizeof(params),
             "sender_ns_fd=%d receiver_ns_fd=%d sender_ifname=%s receiver_ifname=%s verbose_netlink=%d send_init_msg=%d",
             sender_fd, receiver_fd, sender_if, receiver_if, verbose, send_init);

    char cmd[512];
    snprintf(cmd, sizeof(cmd), "insmod ./dd_udp.ko %s", params);
    if (system(cmd) == 0) {
        printf("Module loaded with sender_ns=%s (fd=%d), receiver_ns=%s (fd=%d), sender_ifname=%s, receiver_ifname=%s, verbose_netlink=%d\n",
               sender_ns, sender_fd, receiver_ns, receiver_fd, sender_if, receiver_if, verbose);
    } else {
        perror("Failed to load module (insmod)");
        close(sender_fd);
        close(receiver_fd);
        return 1;
    }

    close(sender_fd);
    close(receiver_fd);
    return 0;
}
