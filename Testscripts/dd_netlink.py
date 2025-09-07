# dd_netlink.py
#
# This file provides Netlink constants & functions
#
import os
import socket
import struct


## Constants
NETLINK_DIODE = 31
NL_CMD_RESET_COUNTERS = 1
NL_CMD_QUERY_COUNTERS = 2
NL_CMD_QUERY_CONFIG   = 3
NL_CMD_SET_CHECKSUM   = 5
NL_CMD_UNSET_CHECKSUM = 6

NLMSG_HDR_FORMAT = 'IHHII'  # length (I), type (H), flags (H), seq (I), pid (I)
NLMSG_HDRLEN = 16           # Size of struct nlmsghdr
NLMSG_PID = os.getpid()     # The script's PID


##
## 'Private' functions
##

## Create and bind a Netlink socket
def __create_netlink_socket():
    sock = socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, NETLINK_DIODE)
    sock.bind((0, 0))  # Bind to PID 0 (kernel assigns a unique PID)
    return sock

## Send a properly formatted Netlink command to the kernel module
def __send_netlink_command(sock, command):
    msg_len = NLMSG_HDRLEN    # Message only consists of Netlink header

    # Pack the header: length, type (command), flags, seq, pid
    msg = struct.pack(NLMSG_HDR_FORMAT, msg_len, command, 0, 0, NLMSG_PID)
    sock.sendto(msg, (0, 0))  # Send the message to the kernel (PID 0)

## Receive and parse the response containing datagram counters from the kernel module
def __receive_counters_response(sock, udp_checksumming):
    data, addr = sock.recvfrom(1024)  # Receive up to 1024 bytes
    if addr[0] != 0:                  # Ensure the sender is the kernel (PID 0)
        return None

    response = data[NLMSG_HDRLEN:].decode().strip()  # Decode bytes to string
    response = response.replace('\x00', '')          # Remove NULL bytes
    parts = response.split(', ')                     # Parse "Sent: X, Received: Y" or "Sent: X, Received: Y, Corrupted: Z"
    sent = int(parts[0].split(': ')[1])
    received = int(parts[1].split(': ')[1])
    if udp_checksumming:
        corrupted = int(parts[2].split(': ')[1])
    else:
        corrupted = "na"   # Without UDP checksumming, set corrupted to 'not available'
    
    return {"sent_datagrams"      : sent, 
            "received_datagrams"  : received, 
            "corrupted_datagrams" : corrupted}

## Receive config response from the kernel module
def __receive_config_response(sock):
    data, addr = sock.recvfrom(1024)  # Receive up to 1024 bytes
    if addr[0] != 0:                  # Ensure the sender is the kernel (PID 0)
        return None

    response = data[NLMSG_HDRLEN:].decode().strip()  # Decode bytes to string
    response = response.replace('\x00', '')          # Remove NULL bytes
    return response


## 
## 'Public' functions
## 

## Initialize Netlink socket
def initialize_netlink_socket():
    return __create_netlink_socket()

## Obtains kernel module config in human readable format
def current_module_config(sock):
    __send_netlink_command(sock, NL_CMD_QUERY_CONFIG)
    return __receive_config_response(sock)

## Sets UDP checksumming to 1/True
def enable_upd_checksum(sock):
    __send_netlink_command(sock, NL_CMD_SET_CHECKSUM)

## Sets UDP checksumming to 0/False
def disable_udp_checksum(sock):
    __send_netlink_command(sock, NL_CMD_UNSET_CHECKSUM)

## Sets datagram counters to 0
def reset_datagram_counters(sock):
    __send_netlink_command(sock, NL_CMD_RESET_COUNTERS)

## Query datagram counters from kernel module
def query_datagram_counters(sock, udp_checksumming):
     __send_netlink_command(sock, NL_CMD_QUERY_COUNTERS)
     return __receive_counters_response(sock, udp_checksumming)

## Close Netlink socket
def close_netlink_socket(sock):
    sock.close()

