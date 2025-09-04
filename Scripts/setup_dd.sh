#
# Setupscript for use on GMKtec NucBox M5 plus.
# (AMD Ryzen 7 5825U Mini PC with two 2.5Gbps NICs, running Kubuntu 24.04 LTS)
#
#  Device-1: Realtek RTL8125 2.5GbE driver: r8169 - IF: enp1s0
#  Device-2: Realtek RTL8125 2.5GbE driver: r8169 - IF: enp2s0 (<MAC_ADDRESS>)
#
# Device-1 will be the sender, Device-2 will act as the receiver.
# A network namespace for each NIC.
#

# Creating network namespaces
sudo ip netns add sender_ns
sudo ip netns add receiver_ns

# Moving NICs to namespaces
sudo ip link set enp1s0 netns sender_ns
sudo ip link set enp2s0 netns receiver_ns

# Setting IP addresses
sudo ip netns exec sender_ns ip addr add 10.0.1.2/24 dev enp1s0
sudo ip netns exec receiver_ns ip addr add 10.0.1.1/24 dev enp2s0

# Bring interfaces up
sudo ip netns exec sender_ns ip link set enp1s0 up
sudo ip netns exec receiver_ns ip link set enp2s0 up

# Adding route in sender_ns to enp2s0
sudo ip netns exec sender_ns ip route add 10.0.1.1 dev enp1s0

# Set ARP entry for enp2s0
sudo ip netns exec sender_ns ip neigh add 10.0.1.1 lladdr <MAC_ADDRESS> dev enp1s0

#
# Testing with nc:
#
# sudo ip netns exec receiver_ns nc -ul -p 12345
# echo "Hello, Data Diode!" | sudo ip netns exec sender_ns nc -u 10.0.1.1 12345
#
