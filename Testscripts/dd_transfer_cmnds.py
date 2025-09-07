# dd_transfer_cmnds.py
#
# This file provides send and receive functionality
#
import subprocess

from dd_config import *      # imports config settings


## Import diode/network settings
TX_NAMESPACE = common_config['TX_NAMESPACE']
RX_NAMESPACE = common_config['RX_NAMESPACE']
TX_IP        = common_config['TX_IP']
RX_IP        = common_config['RX_IP']
TX_NIC_IF    = common_config['TX_NIC_IF']
RX_NIC_IF    = common_config['RX_NIC_IF']

TOOLS_SUPPORTED = common_config['TOOLS']

## Import nc settings
NC           = nc_config['NC']
NC_RX_PORT   = nc_config['RX_PORT']
RATE_LIMITER = nc_config['RATE_LIMITER']
CHUNK_SIZE   = nc_config['CHUNK_SIZE']

# Pydiode settings
PYDIODE = pydiode_config['PYDIODE']


## Is tool supported?
def __check_tool(tool):
    if tool not in TOOLS_SUPPORTED:
        raise(f"TOOL {tool} NOT SUPPORTED!")


## 
## 'Private' NC send and receive commands
## 

## Start NC receive command and return process handle
def __start_nc_receive_process(file_out):
    command = ["sudo", "ip", "netns", "exec", RX_NAMESPACE, NC, "-w", "1", "-ul", "-p", NC_RX_PORT]
    with open(file_out, "wb") as outfile:
        receive_process = subprocess.Popen(command, stdout=outfile, text=False)
    return receive_process

## Build & start sending process; returns process handle
def __start_nc_send_process(file_in, bitrate):
    with open(file_in, "rb") as infile:
        if RATE_LIMITER == 'pv':
            pv_process = subprocess.Popen(["pv", "--si", "--rate-limit", str(bitrate // 8)], stdin=infile, 
                                    stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=False)
        elif RATE_LIMITER == 'throttler.py':
            pv_process = subprocess.Popen(["./throttler.py", "-c", str(CHUNK_SIZE), "-b", str(bitrate)], 
                                    stdin=infile, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=False)
        elif RATE_LIMITER == 'regulator.py':
            chunk_rate = str(bitrate/(CHUNK_SIZE * 8))
            pv_process = subprocess.Popen(["./regulator.py", "--chunk-size", str(CHUNK_SIZE), 
                                    "--chunk-rate", chunk_rate], 
                                    stdin=infile, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=False)
        
        send_process = subprocess.Popen(["sudo", "ip", "netns", "exec", TX_NAMESPACE, NC, "-u", "-q", 
                                       "1", RX_IP, NC_RX_PORT], stdin=pv_process.stdout, text=False)
        send_process.communicate()
    return send_process


## 
## 'Private' pydiode send and receive commands
## 

## Start pydiode receive command and return process handle
def __start_pydiode_receive_process(file_out):
    command = ["sudo", "ip", "netns", "exec", RX_NAMESPACE, PYDIODE, "receive", RX_IP]
    with open(file_out, "wb") as outfile:
        receive_process = subprocess.Popen(command, stdout=outfile, text=False)
    return receive_process

## Build & start pydiode sending process; returns process handle
def __start_pydiode_send_process(file_in, bitrate, redundancy):
    command = ["sudo", "ip", "netns", "exec", TX_NAMESPACE, PYDIODE, "send",
               RX_IP, TX_IP , "--max-bitrate", str(bitrate), "--redundancy", redundancy]
    with open(file_in, "rb") as infile:
        send_process = subprocess.run(command, stdin=infile, text=False)
    return send_process


## 
## 'Public' generic send and receive commands
## 

## Start correct receive command and return process handle
def start_receive_process(tool, file_out):
    __check_tool(tool)
    if tool == 'nc':
        receive_process = __start_nc_receive_process(file_out)
    elif tool == 'pydiode':
        receive_process = __start_pydiode_receive_process(file_out)
    return receive_process

## Build & start correct sending process; returns process handle
def start_send_process(tool, file_in, bitrate, redundancy=None, fec=None):
    __check_tool(tool)
    if tool == 'nc':
        send_process = __start_nc_send_process(file_in, bitrate)
    elif tool == 'pydiode':
        if not redundancy: 
            raise("Redundancy mandatory when testing with pydiode!")
        send_process = __start_pydiode_send_process(file_in, bitrate, redundancy)
    return send_process
