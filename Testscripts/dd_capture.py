# dd_capture.py
#
# This file provides packet capturing functionality
#
import glob
import os
import subprocess

from scapy.all import *
from scapy.layers.inet import UDP

from dd_config import *      # imports config settings


## Import diode/network settings
TX_NAMESPACE = common_config['TX_NAMESPACE']
RX_NAMESPACE = common_config['RX_NAMESPACE']
TX_NIC_IF    = common_config['TX_NIC_IF']
RX_NIC_IF    = common_config['RX_NIC_IF']

TCPDUMP_ANALYSIS     = common_config['TCPDUMP_ANALYSIS']
TCPDUMP_ECONOMY_MODE = common_config['TCPDUMP_ECONOMY_MODE']

FILE_OUT_BASE = common_config['FILE_OUT_BASE']

FILE_IN_SIZE = common_config['FILE_IN_SIZE']
BUFFER_SIZE  = str((int(FILE_IN_SIZE)+5000)/1000)  # TCPDump buffer 5MB bigger than file size


#
# 'Private' functions
#

## Run tcpdump to capture UDP traffic on the specified interface
def __start_capture(namespace, interface, pcap_file, direction):
    cmd = f"sudo ip netns exec {namespace} tcpdump -i {interface} -n -B {BUFFER_SIZE} -s 0 -w {pcap_file} 'udp and {direction}'"
    process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    return process.pid

## Kill all (tcpdump) process tree for parent_pid
def __stop_capture(namespace, parent_pid):
    try:
        cmd = f"sudo ip netns exec {namespace} pkill -P {parent_pid}"
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to kill process tree for PID {parent_pid}. Details: {e}")

## Returns all UDP packets found in pcap_file
def __analyse_pcap(pcap_file):
    packets = rdpcap(pcap_file)
    udp_packets = [pkt for pkt in packets if pkt.haslayer(UDP)]
    return udp_packets, len(packets)

## Move captures to given directory
def __move_captures(captures_dir):
    os.makedirs(captures_dir, exist_ok=True)
    for file in glob("*.pcap"):
        subprocess.run(f"mv {file} {captures_dir}/{file}", shell=True, check=True)

## Delete .pcap files
def __delete_captures():
    for file in glob("*.pcap"):
        os.remove(file)


#
# 'Public' functions
#

## Start tcpdump in sender namespace
def start_sender_capture(file):
    return __start_capture(TX_NAMESPACE, TX_NIC_IF, file, 'outbound')

## Start tcpdump in receiver namespace
def start_receiver_capture(file):
    return __start_capture(RX_NAMESPACE, RX_NIC_IF, file, 'inbound')

## Stop the tcpdump captures and organize resulting pcap files
def stop_and_organize_captures(sender_pid, receiver_pid, captures_dir):
    __stop_capture(RX_NAMESPACE, receiver_pid)
    __stop_capture(TX_NAMESPACE, sender_pid)
    __move_captures(captures_dir)

## Stop the tcpdump captures and delete resulting pcap files
def stop_and_delete_captures(sender_pid, receiver_pid):
    __stop_capture(RX_NAMESPACE, receiver_pid)
    __stop_capture(TX_NAMESPACE, sender_pid)
    __delete_captures()

## Counts the UDP packets in sender and receiver captures
def check_packetloss(file_sent, file_recv, captures_dir, trial):
    sender_packets, sent = __analyse_pcap(f"{captures_dir}/{file_sent}")
    receiver_packets, received = __analyse_pcap(f"{captures_dir}/{file_recv}")
    send_count = len(sender_packets)
    received_count = len(receiver_packets)
    loss_count = send_count - received_count

    print(f"tcpdump - Trial: {trial:04d} - UDP Sent: {send_count}, Received: {received_count}, Lost: {loss_count}; Total sent: {sent}, Total received: {received}, Lost: {received-sent}")
    return loss_count

## Start tcp captures
def start_tcp_captures(tool_str, file_suffix):
    capture_sent = f"in_{FILE_OUT_BASE}_{tool_str}_{file_suffix}.pcap"
    capture_recv = f"out_{FILE_OUT_BASE}_{tool_str}_{file_suffix}.pcap"
    receiver_capture_pid = start_receiver_capture(capture_recv)
    sender_capture_pid = start_sender_capture(capture_sent)
    return {"capture_sent"         : capture_sent, 
            "capture_recv"         : capture_recv, 
            "receiver_capture_pid" : receiver_capture_pid, 
            "sender_capture_pid"   : sender_capture_pid}

## End captures and organize them properly
def stop_tcp_captures(captures_dict, captures_dir, transfer_succes, trial):
    if transfer_succes and TCPDUMP_ECONOMY_MODE:
        stop_and_delete_captures(captures_dict['sender_capture_pid'], 
                                 captures_dict['receiver_capture_pid'])
    if transfer_succes and not TCPDUMP_ECONOMY_MODE:
        stop_and_organize_captures(captures_dict['sender_capture_pid'], 
                                   captures_dict['receiver_capture_pid'], 
                                   captures_dir)
        if TCPDUMP_ANALYSIS: 
            check_packetloss(captures_dict['capture_sent'], 
                             captures_dict['capture_recv'], 
                             captures_dir, trial)
    elif not transfer_succes:
        stop_and_organize_captures(captures_dict['sender_capture_pid'], 
                                   captures_dict['receiver_capture_pid'], 
                                   captures_dir)
        if TCPDUMP_ANALYSIS: 
            check_packetloss(captures_dict['capture_sent'], 
                             captures_dict['capture_recv'], 
                             captures_dir, trial)

