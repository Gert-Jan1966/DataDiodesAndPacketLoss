# Tips & Tricks Test Setup

The test setup consists of a NUC with two 2.5 Gbit RJ45 NICs.
These two ports are interconnected via a simple data diode setup consisting of two media converters (copper/fiber), which are connected to each other using a fiber optic cable. The OS used is (K)ubuntu 24.04 LTS.

---

## Network Settings

1. Ensure that **at least** one of the NICs is placed in a separate Linux Network Namespace. Otherwise, the data traffic bypasses the setup and goes ‘through the Linux kernel’.
2. For this research, both NICs are placed in their own separate namespaces. This leaves the default namespace available exclusively for data traffic over the NUC’s WiFi connection.

---

## NUC/PC Settings

1. **sudo privileges**
   To use tools like netcat/nc, pydiode, and UDPcast within the network namespaces, they must be started with ‘sudo’. It’s annoying to repeatedly enter the sudo password. Using **sudo visudo**, you can modify the validity period of ‘sudo’:

   * **\$ sudo visudo** opens a Nano editor window.
   * Under the first ‘Defaults’ section, add: **Defaults timestamp\_timeout=`time-in-minutes`**
   * Exit Nano with ^X and confirm saving the file.
   * Reboot the machine—this new sudo timeout will apply to all terminal sessions.
     **NOTE:** This change applies to **all sudoers** on the Linux machine!

2. **tcpdump processes**
   To capture packets, **tcpdump** is used within the namespaces of the NICs.
   It turned out that subprocesses launched by the Python scripts could not be properly terminated.
   The **AppArmor** settings in **(K)ubuntu 24.04** were the culprit. These can be **permanently** disabled using:

   * `$ sudo ln -s /etc/apparmor.d/usr.bin.tcpdump /etc/apparmor.d/disable/`
   * `$ sudo apparmor_parser -R /etc/apparmor.d/usr.bin.tcpdump`
   * `$ sudo systemctl reload apparmor`

---

## Tools

1. **UDPcast**
   So far, UDPcast has proven to be a ‘problematic’ tool. It produces a lot of console output and frequently fails during tests without meaningful error messages. From examining the UDPcast source code:

   * Any error leads UDPcast to exit with code "1".
   * Errors are described via **stdout/stderr**.
   * UDPcast only returns "0" when everything succeeds; any failure returns "1", regardless of the type.

2. **tcpdump and timing**
   These processes not only take some time to start but also require proper shutdown to ensure that:

   * The resulting pcap files are valid.
   * The packet counts are accurate.
   * Add 'sleep' statements in the calling scripts where needed to allow for this.

3. **tcpdump within the “Vrolijk setup”** (media converters with Y-cable)
   On the sending side (inbound side of the diode), use tcpdump with the option **‘udp and outbound’**.
   Due to the *loopback* created by the fiber Y-splitter, the sent packets also return to the sending NIC.
   Without the **and outbound** option, these returning packets are also counted, resulting in double packet counts.

4. **tcpdump and capture file size**
   Naturally, capture files are **greater than or equal to** the size of the files sent. Keep this in mind when running large test batches!

   * Example: with pydiode and a redundancy setting of 2, sending a 125MB file results in two pcap files of approximately 252MB each.
   * Counting packets in a 125MB pcap file takes around 10 seconds—per test case, this adds **at least 20 seconds** to the total test duration!


