# dd_udp: UDP Linux kernel module for Data Diodes
This is a basic/lightweight alternative kernel module for UDP data traffic **within** data diodes.<br>
This module offers Netlink based messaging between kernel space and userland. This message traffic is primarily intended to reset and read datagram counters within the module. This kernel module can detect corrupted datagrams based on UDP checksumming, taking NIC offloading into account.

## Preliminary remarks
- The module has been tested on a NUC with 2 NIC's.
- Use the **load_diode** utility for easy loading into the kernel.
- 2 Linux network namespaces are supported (look for `../../Scripts/setup_dd.sh` within this repo).
- The datagram counters can be reset and queried from testscripts (**sent**, **received** and **corrupted** datagrams) using Netlink messages.
- UDP checksumming can be enabled/disable using Netlink messages.

## The files
- **dd_udp.c**
  * The C code for the module.
- **Makefile**
  * Makefile for dd_udp.c.
- **load_diode.c**
  * Utility to load the module.

## Compile/build instructions
- Build load_diode.c: <br>
  `$ gcc -o load_diode load_diode.c`

- Build dd_udp.c: <br>
  `$ make clean && make`

## Using/testing the dd_udp module
These steps assume testing on a NUC with 2 network ports, connected using diode hardware.

- Initialize diode setup: <br>
  `$ setup_dd.sh`

- Initialize kernel message buffer: <br>
  `$ sudo dmesg -C`
  
- Load the kernel module:<br>
  `$ sudo ./load_diode -n sender_ns_name receiver_ns_name sender_if-name receiver_if-name`<br>
  Please provide the correct **ns**- and **if**-names, otherwise the data traffic may skip the NIC's and may only travel 
  "through the kernel".<br> 

- When loaded correctly, a conformation like this appears:
```
Module loaded with sender_ns=sender_ns (fd=3), receiver_ns=receiver_ns (fd=4), sender_ifname=enp1s0, receiver_ifname=enp2s0, verbose_netlink=0
```

- Checking the kernel messages with `$ sudo dmesg` should return output like:
```
[   80.351766] dd_udp: loading out-of-tree module taints kernel.
[   80.351772] dd_udp: module verification failed: signature and/or required key missing - tainting kernel
[   80.352160] dd_udp: Registered sender hook for sender FD 3, sender_if enp1s0
[   80.352177] dd_udp: Registered receiver hook for receiver FD 4, receiver_if enp2s0
[   80.352179] dd_udp: Loaded with sender FD 3 -> receiver FD 4, sender_if enp1s0, receiver_if enp2s0
```
- A quick test using 2 Linux terminals:
  * `$ sudo ip netns exec receiver_ns nc -ul -p 12345`
  * `$ echo "Hello, Data Diode!" | sudo ip netns exec sender_ns nc -u 10.0.1.1 12345`

  Provided all works well, the text `Hello, Data Diode!` should appear in the receiver_ns terminal.

- To remove the dd_udp module from the kernel:
  * Quit any instances of netcat and/or Python scripts with `^C`.
  * `$ sudo rmmod dd_udp`

## Options of the load_diode utility
```
$ ./load_diode -h
Usage: ./load_diode [-h] [-n] [-v] <sender_ns> <receiver_ns> [sender_ifname] [receiver_ifname]

Loads the dd_udp kernel module with specified namespaces and interfaces.

Options and Arguments:
  -h              Display this help message and exit.
  -n              Disable sending the initial 'module loaded' Netlink message.
  -v              Enable verbose Netlink messaging for accepted/received UDP packets.
  sender_ns       Name of the sender namespace (e.g., sender_ns).
  receiver_ns     Name of the receiver namespace (e.g., receiver_ns).
  sender_ifname   (Optional) Sender interface name (e.g., enp1s0). Default: eth0
  receiver_ifname (Optional) Receiver interface name (e.g., enp6s0). Default: eth1

Examples:
  ./load_diode sender_ns receiver_ns
  ./load_diode -n sender_ns receiver_ns enp1s0 enp6s0
  ./load_diode -n -v sender_ns receiver_ns enp1s0 enp6s0
````
