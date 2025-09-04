sudo ip netns exec sender_ns ip link set dev enp1s0 mtu 9194
sudo ip netns exec receiver_ns ip link set dev enp2s0 mtu 9194
