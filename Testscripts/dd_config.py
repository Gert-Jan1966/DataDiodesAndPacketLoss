# dd_config.py
#
# Settings for the testscripts
#

## Common settings
common_config = {
    'DEFAULT_UDP_MODULE' : 1,   # 1 = on; 0 = dd_udp.c module

    'TOOL2RUN' : 'pydiode', 
    'TOOLS'    : ('nc', 'pydiode'), 
    'BITRATES' : (1000000000, 750000000, 500000000, 250000000, 100000000), 
    'TRIALS'   : 1000, 

    'UDP_CHECKSUMMING'     : 0,   # 1 = on; 0 = off
    'TCPDUMP_ENABLED'      : 0,   # 1 = on; 0 = off
    'TCPDUMP_ANALYSIS'     : 0,   # 1 = on; 0 = off
    'TCPDUMP_ECONOMY_MODE' : 0,   # 1 = on; 0 = off; Saves recources (storage and cpu time)

    'TX_NIC_IF'    : 'enp1s0', 
    'RX_NIC_IF'    : 'enp2s0', 
    'TX_NAMESPACE' : "sender_ns", 
    'RX_NAMESPACE' : "receiver_ns", 
    'TX_IP'        : "10.0.1.2", 
    'RX_IP'        : "10.0.1.1", 

    'TESTRESULTS_DIR_PREFIX' : '../TESTRESULTS', 
    'FILE_IN'       : "test_data",  # "/tmp/random_data", 
    'FILE_IN_SIZE'  : "125000000",  # 1Gbit = 125000000bytes
    'FILE_OUT_BASE' : "testdata"
}

## nc settings
nc_config = {
    'NC'           : "nc", 
    #'RATE_LIMITER' : 'regulator.py',
    #'RATE_LIMITER' : 'pv', 
    'RATE_LIMITER' : 'throttler.py', 
    'RX_PORT'      : "50000",
    'CHUNK_SIZE'   : 16384 #16384 9166 # Data segment size for use with regulator.py or throttler.py
}

## pydiode settings
pydiode_config = {
    'PYDIODE'      : "/home/gertjan/.local/bin/pydiode", 
    'REDUNDANCIES' : ("2", "1") 
}
