# dd_link_layer_stats.py
#
# This file provides monitoring functionality of TX and RX NIC buffers
#
import subprocess

from dd_config import *  # imports config settings


## Import diode/network settings
TX_NAMESPACE = common_config['TX_NAMESPACE']
RX_NAMESPACE = common_config['RX_NAMESPACE']
TX_NIC_IF = common_config['TX_NIC_IF']
RX_NIC_IF = common_config['RX_NIC_IF']


#
# 'Private' functions
#

## Returns specific stat for given namespace and interface
def __get_nic_stats(namespace, interface, stat_name):
    cmd = f"sudo ip netns exec {namespace} cat /sys/class/net/{interface}/statistics/{stat_name}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        return int(result.stdout.strip())
    else:
        raise RuntimeError(f"Failed to get {stat_name} for {interface} in {namespace}")

def __get_tx_errors():
    return __get_nic_stats(TX_NAMESPACE, TX_NIC_IF, 'tx_errors')

def __get_tx_dropped():
    return __get_nic_stats(TX_NAMESPACE, TX_NIC_IF, 'tx_dropped')

def __get_rx_errors():
    return __get_nic_stats(RX_NAMESPACE, RX_NIC_IF, 'rx_errors')

def __get_rx_dropped():
    return __get_nic_stats(RX_NAMESPACE, RX_NIC_IF, 'rx_dropped')


#
# 'Public' functions
# 

## Get stats of both rx and tx buffers
def get_all_link_layer_stats():
    return {'rx_errors' : __get_rx_errors(), 
            'rx_dropped': __get_rx_dropped(), 
            'tx_errors' : __get_tx_errors(), 
            'tx_dropped': __get_tx_dropped()}

## Calculate relevant statistics
def compute_link_layer_stats(results_start, results_end):
    return {
        "tx_errors"  : results_end['tx_errors']  - results_start['tx_errors'], 
        "tx_dropped" : results_end['tx_dropped'] - results_start['tx_dropped'], 
        "rx_errors"  : results_end['rx_errors']  - results_start['rx_errors'], 
        "rx_dropped" : results_end['rx_dropped'] - results_start['rx_dropped']
    }

