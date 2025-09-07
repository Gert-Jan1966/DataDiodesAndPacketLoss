#!/usr/bin/python3
import os
import time

from datetime import datetime

from dd_capture import *                # import for packet capturing
from dd_common import *                 # imports common functions
from dd_config import *                 # imports config settings
from dd_netlink import *                # imports custom Netlink functionality
from dd_statistics import *             # imports custom statistics functionality
from dd_transfer_cmnds import *         # imports receive and send commands
from dd_link_layer_stats import *       # imports TX and RX NIC buffer monitoring
from dd_transport_layer_stats import *  # imports monitoring /proc/net/snmp functions


## Tool settings
TOOL                 = common_config['TOOL2RUN']
DEFAULT_UDP_MODULE   = common_config['DEFAULT_UDP_MODULE']
UDP_CHECKSUMMING     = common_config['UDP_CHECKSUMMING']
TCPDUMP_ENABLED      = common_config['TCPDUMP_ENABLED']

## Import other test settings
REDUNDANCIES = pydiode_config['REDUNDANCIES']
BITRATES     = common_config['BITRATES']
TRIALS       = common_config['TRIALS']

FILE_IN       = common_config['FILE_IN']
FILE_IN_SIZE  = common_config['FILE_IN_SIZE']
FILE_OUT_BASE = common_config['FILE_OUT_BASE']
TESTRESULTS_DIR_PREFIX = common_config['TESTRESULTS_DIR_PREFIX']

## Other constants
TEST_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")  # Timestamp start testrun
SENT_HASH = create_testfile(FILE_IN, FILE_IN_SIZE)         # Create fixed sourcedata and calculate hash
RESULTS_DIR = f"{TESTRESULTS_DIR_PREFIX}_{TEST_TIMESTAMP}"
CAPTURES_DIR = f"{RESULTS_DIR}/captures"


#
## Functions
# 

## Run every trail for a bitrate
def run_trials(bitrate, sock, tool, redundancy=None):
    transfer_results = []  # Initializing for statistics

    for trial in range(TRIALS):
        print(f"\033[2K\rTrial: {trial:4d}", end='', flush=True)  # Print trial 'counter' on the cli/stdout

        ## Build output and pcap filenames
        file_suffix = f"{trial:04d}_{bitrate}"
        file_out = f"{FILE_OUT_BASE}_{file_suffix}"

        ## Determine part of output- and pcap filenames    
        tool_str = get_tool_str(tool, redundancy)

        ## Start receiver process
        receive_process = start_receive_process(tool, file_out)
        time.sleep(2)

        if not DEFAULT_UDP_MODULE:
            reset_datagram_counters(sock)  # Reset counters before transmission

        ## Start tcp dump captures if enabled
        if TCPDUMP_ENABLED:
            captures_dict = start_tcp_captures(tool_str, file_suffix)
            time.sleep(2)
        
        link_layer_stats_start = get_all_link_layer_stats()            # Get starting values from the TX and RX buffers
        transport_layer_stats_start = get_all_transport_layer_stats()  # Get starting values Transport Layer stats

        ## Start sender process
        send_time = time.time()     # Get send timestamp
        send_process = start_send_process(tool, FILE_IN, bitrate, redundancy=redundancy)
        receive_process.wait()      # Wait for the receiver process to complete
        receive_time = time.time()  # Get receive timestamp

        transfer_succes = SENT_HASH == hash_file(file_out)

        ## Stop tcp dump captures (if enabled)
        if TCPDUMP_ENABLED:
            time.sleep(2)
            stop_tcp_captures(captures_dict, CAPTURES_DIR, transfer_succes, trial)

        ## Query module counters after transmission; 'na' values if testing on default udp.c module
        if not DEFAULT_UDP_MODULE:
            kernel_stats = query_datagram_counters(sock, UDP_CHECKSUMMING)
        else:
            kernel_stats = {"sent_datagrams": 'na', "received_datagrams": 'na', "corrupted_datagrams": 'na'}

        transport_layer_stats_end = get_all_transport_layer_stats()  # Get final stats from the Transport Layer
        transport_layer_stats = compute_transport_layer_stats(transport_layer_stats_start, transport_layer_stats_end)

        link_layer_stats_end = get_all_link_layer_stats()  # Get the final stats from the TX and RX buffers
        link_layer_stats = compute_link_layer_stats(link_layer_stats_start, link_layer_stats_end)

        ## Save results for this test
        transfer_results.append({
                    "bitrate":           bitrate, 
                    "trial":             trial, 
                    "sender_rc":         send_process.returncode,
                    "receiver_rc":       receive_process.returncode,
                    "Xfer_time":         receive_time - send_time, 
                    "Xfer_success":      transfer_succes, 
                    "in_file_size":      FILE_IN_SIZE, 
                    "out_file_size":     os.path.getsize(file_out), 
                    "dtgrms_sent":       kernel_stats['sent_datagrams'], 
                    "dtgrms_received":   kernel_stats['received_datagrams'], 
                    "dtgrms_corrupt":    kernel_stats['corrupted_datagrams'],
                    "tx_errors":         link_layer_stats['tx_errors'],
                    "tx_dropped":        link_layer_stats['tx_dropped'],
                    "rx_errors":         link_layer_stats['rx_errors'],
                    "rx_dropped":        link_layer_stats['rx_dropped'], 
                    "snmp_OutDatagrams": transport_layer_stats['OutDatagrams'], 
                    "snmp_SndbufErrors": transport_layer_stats['SndbufErrors'], 
                    "snmp_InDatagrams":  transport_layer_stats['InDatagrams'], 
                    "snmp_InErrors"   :  transport_layer_stats['InErrors'], 
                    "snmp_RcvbufErrors": transport_layer_stats['RcvbufErrors']})


    print(f"\033[2K\r", end='', flush=True)   # 'Remove' the trial counter from the cli/stdout

    ## Persist output data in csv-file
    output_filename = f"testresults_{tool_str}_{bitrate}.csv"
    output_2_csv(transfer_results, output_filename, RESULTS_DIR)
    print_simple_statistics(transfer_results)  # Print results to stdout


## Perform all trails for each bitrate
def test_bitrates(bitrates, sock, tool, redundancy=None):
    for bitrate in bitrates:
        print(f"Bitrate: {bitrate} bits/second")
        if output_files_exist(FILE_OUT_BASE):
            delete_output_files(FILE_OUT_BASE)       # Remove output from previous testruns
        run_trials(bitrate, sock, tool, redundancy)  # Run all trials for this bitrate


## Perform test for each redundancy (pydiode)
def test_redundancies(redundancies, sock, tool):
    for redundancy in redundancies:
        print(f"\nRedundancy: {redundancy}\n")
        test_bitrates(BITRATES, sock, tool, redundancy)  # Run test for all bitrates for this redundancy


#
## Main script
#

## Checks with module is loaded and get Netlink socket if available
if not DEFAULT_UDP_MODULE:
    try:
        sock = initialize_netlink_socket()
        enable_upd_checksum(sock) if UDP_CHECKSUMMING else disable_udp_checksum(sock)
    except:
        print("No Netlink socket available; did you load the dd_udp.c kernel module?")
        exit(1)
else:  # Default UDP module check
    try:
        sock = initialize_netlink_socket()
    except:
        sock = None
    if sock:
        print("dd_udp.c kernel module is loaded, cannot test with default UDP.c kernel module.")
        exit(1)

## Get & print the kernel module's settings
print(f"\nCurrent kernel module config:")
if not DEFAULT_UDP_MODULE:
    print(f"dd_udp.c - {current_module_config(sock)}\n")
else:
    print("Default UDP.c kernel module\n")
print("Test results\n------------")

## Test tool selection
if TOOL == 'pydiode':
    test_redundancies(REDUNDANCIES, sock, TOOL)
elif TOOL == 'nc':
    test_bitrates(BITRATES, sock, TOOL)

## Clean up
delete_output_files(FILE_OUT_BASE)

if not DEFAULT_UDP_MODULE:
    close_netlink_socket(sock)
