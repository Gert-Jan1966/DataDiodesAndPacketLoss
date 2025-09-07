# dd_transport_layer_stats.py
#
# This module accesses /proc/net/snmp for UDP statistics
#
import subprocess

from dd_config import *  # imports config settings


## Import diode/network settings
TX_NAMESPACE = common_config['TX_NAMESPACE']
RX_NAMESPACE = common_config['RX_NAMESPACE']


#
# 'Private' functions
#

## Gets the "Udp: " stats from /proc/net/smnp
def __get_udp_stats(namespace):
    cmd = ["sudo", "ip", "netns", "exec", namespace, "cat", "/proc/net/snmp"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)

    lines = [line for line in result.stdout.splitlines() if line.startswith("Udp:")]
    if len(lines) < 2:
        raise RuntimeError("Unexpected output format from /proc/net/snmp")

    keys = lines[0].split()[1:]   # Skip "Udp:"
    values = lines[1].split()[1:] # Skip "Udp:"

    return dict(zip(keys, map(int, values)))


#
# 'Public' functions
#

## Get all relevant UDP statistics
def get_all_transport_layer_stats():
    return {'sent' : __get_udp_stats(TX_NAMESPACE), 
            'recv' : __get_udp_stats(RX_NAMESPACE)}

## Calculate relevant statistics
def compute_transport_layer_stats(results_start, results_end):
    return {
        "OutDatagrams" : results_end['sent']['OutDatagrams'] - results_start['sent']['OutDatagrams'], 
        "SndbufErrors" : results_end['sent']['SndbufErrors'] - results_start['sent']['SndbufErrors'], 
        "InDatagrams"  : results_end['recv']['InDatagrams']  - results_start['recv']['InDatagrams'], 
        "InErrors"     : results_end['recv']['InErrors']     - results_start['recv']['InErrors'], 
        "RcvbufErrors" : results_end['recv']['RcvbufErrors'] - results_start['recv']['RcvbufErrors']
    }

