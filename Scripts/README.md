# Scripts
These are simple Bash scripts. Please adjust the namespace names, if-names, IP addresses and/or MAC adress to your own needs.

---

## setup_dd.sh
This Linux shell script initialises Linux network namespaces and the NIC's in the data diode testing setup.

## disable-apparmor-tcpdump-profile.sh
Use this script to disable the apparmor tcpdump profile on recent Ubuntu based setups.<br>
<br>
The use case for this script:
- On Kubuntu 24.04 LTS, I was able to start tcpdump processes from Python but was not able to end/remove those processes.

## rbuffer-XXmb.sh
These scripts increase the UDP receiver socket buffer to XX Mebibytes.

## mtu-YYYY.sh
These scripts set the MTU values on both NICs to YYYY bytes.

