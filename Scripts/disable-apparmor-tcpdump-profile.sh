#
# Disables AppArmor profile for tcpdump - (K)Ubuntu 24.04
#
sudo ln -s /etc/apparmor.d/usr.bin.tcpdump /etc/apparmor.d/disable/
sudo apparmor_parser -R /etc/apparmor.d/usr.bin.tcpdump
sudo aa-status | grep tcpdump
sudo systemctl reload apparmor
