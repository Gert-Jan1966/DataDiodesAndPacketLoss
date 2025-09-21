# Notebooks

This directory contains Jupyter notebooks used for analysing `Testresults`.<br>
The tables below serve as indexes for easier navigation through the subdirectories.

---

### Baseline test results
These tests were conducted with the default socket buffer sizes of 208 KiB

| Tool                  | Kernel module | Notebook |
| ---                   | :---:         | ---      |
| Netcat                | UDP.c         | [NC-default-tests.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/baseline/NC-default-tests.ipynb) |
| Netcat                | dd_udp.c      | [NC-dd_udp-tests.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/baseline/NC-dd_udp-tests.ipynb) |
| pydiode; redundancy=1 | UDP.c         | [pydiode-1-default-tests.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/baseline/pydiode-1-default-tests.ipynb) |
| pydiode; redundancy=1 | dd_udp.c      | [pydiode-1-dd_udp-tests.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/baseline/pydiode-1-dd_udp-tests.ipynb) |
| pydiode; redundancy=2 | UDP.c         | [pydiode-2-default-tests.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/baseline/pydiode-2-default-tests.ipynb) |
| pydiode; redundancy=2 | dd_udp.c      | [pydiode-2-dd_udp-tests.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/baseline/pydiode-2-dd_udp-tests.ipynb) |


---


### Test results for increased UDP receiver socket buffer

| Buffer size | Tool                  | Kernel module | Notebook |
| ---:     | ---                   | :---:         | ---      |
| 1 MiB    | Netcat                | UDP.c         | [NC-default-recbuf-1MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-01MiB/NC-default-recbuf-1MiB.ipynb) |
| 1 MiB    | Netcat                | dd_udp.c      | [NC-dd_udp-recbuf-1MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-01MiB/NC-dd_udp-recbuf-1MiB.ipynb) |
| 1 MiB    | pydiode; redundancy=1 | UDP.c         | [pydiode-1-default-recbuf-1MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-01MiB/pydiode-1-default-recbuf-1MiB.ipynb) |
| 1 MiB    | pydiode; redundancy=1 | dd_udp.c      | [pydiode-1-dd_udp-recbuf-1MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-01MiB/pydiode-1-dd_udp-recbuf-1MiB.ipynb) |
| 1 MiB    | pydiode; redundancy=2 | UDP.c         | [pydiode-2-default-recbuf-1MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-01MiB/pydiode-2-default-recbuf-1MiB.ipynb) |
| 1 MiB    | pydiode; redundancy=2 | dd_udp.c      | [pydiode-2-dd_udp-recbuf-1MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-01MiB/pydiode-2-dd_udp-recbuf-1MiB.ipynb) |
| 2 MiB    | Netcat                | UDP.c         | [NC-default-recbuf-2MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-02MiB/NC-default-recbuf-2MiB.ipynb) |
| 2 MiB    | Netcat                | dd_udp.c      | [NC-dd_udp-recbuf-2MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-02MiB/NC-dd_udp-recbuf-2MiB.ipynb) |
| 2 MiB    | pydiode; redundancy=1 | UDP.c         | [pydiode-1-default-recbuf-2MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-02MiB/pydiode-1-default-recbuf-2MiB.ipynb) |
| 2 MiB    | pydiode; redundancy=1 | dd_udp.c      | [pydiode-1-dd_udp-recbuf-2MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-02MiB/pydiode-1-dd_udp-recbuf-2MiB.ipynb) |
| 2 MiB    | pydiode; redundancy=2 | UDP.c         | [pydiode-2-default-recbuf-2MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-02MiB/pydiode-2-default-recbuf-2MiB.ipynb) |
| 2 MiB    | pydiode; redundancy=2 | dd_udp.c      | [pydiode-2-dd_udp-recbuf-2MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-02MiB/pydiode-2-dd_udp-recbuf-2MiB.ipynb) |
| 4 MiB    | Netcat                | UDP.c         | [NC-default-recbuf-4MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-04MiB/NC-default-recbuf-4MiB.ipynb) |
| 4 MiB    | Netcat                | dd_udp.c      | [NC-dd_udp-recbuf-4MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-04MiB/NC-dd_udp-recbuf-4MiB.ipynb) |
| 4 MiB    | pydiode; redundancy=1 | UDP.c         | [pydiode-1-default-recbuf-4MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-04MiB/pydiode-1-default-recbuf-4MiB.ipynb) |
| 4 MiB    | pydiode; redundancy=1 | dd_udp.c      | [pydiode-1-dd_udp-recbuf-4MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-04MiB/pydiode-1-dd_udp-recbuf-4MiB.ipynb) |
| 4 MiB    | pydiode; redundancy=2 | UDP.c         | [pydiode-2-default-recbuf-4MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-04MiB/pydiode-2-default-recbuf-4MiB.ipynb) |
| 4 MiB    | pydiode; redundancy=2 | dd_udp.c      | [pydiode-2-dd_udp-recbuf-4MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-04MiB/pydiode-2-dd_udp-recbuf-4MiB.ipynb) |
| 8 MiB    | Netcat                | UDP.c         | [NC-default-recbuf-8MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-08MiB/NC-default-recbuf-8MiB.ipynb) |
| 8 MiB    | Netcat                | dd_udp.c      | [NC-dd_udp-recbuf-8MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-08MiB/NC-dd_udp-recbuf-8MiB.ipynb) |
| 8 MiB    | pydiode; redundancy=1 | UDP.c         | [pydiode-1-default-recbuf-8MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-08MiB/pydiode-1-default-recbuf-8MiB.ipynb) |
| 8 MiB    | pydiode; redundancy=1 | dd_udp.c      | [pydiode-1-dd_udp-recbuf-8MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-08MiB/pydiode-1-dd_udp-recbuf-8MiB.ipynb) |
| 8 MiB    | pydiode; redundancy=2 | UDP.c         | [pydiode-2-default-recbuf-8MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-08MiB/pydiode-2-default-recbuf-8MiB.ipynb) |
| 8 MiB    | pydiode; redundancy=2 | dd_udp.c      | [pydiode-2-dd_udp-recbuf-8MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-08MiB/pydiode-2-dd_udp-recbuf-8MiB.ipynb) |
| 16 MiB   | Netcat                | UDP.c         | [NC-default-recbuf-16MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-16MiB/NC-default-recbuf-16MiB.ipynb) |
| 16 MiB   | Netcat                | dd_udp.c      | [NC-dd_udp-recbuf-16MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-16MiB/NC-dd_udp-recbuf-16MiB.ipynb) |
| 16 MiB   | pydiode; redundancy=1 | UDP.c         | [pydiode-1-default-recbuf-16MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-16MiB/pydiode-1-default-recbuf-16MiB.ipynb) |
| 16 MiB   | pydiode; redundancy=1 | dd_udp.c      | [pydiode-1-dd_udp-recbuf-16MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-16MiB/pydiode-1-dd_udp-recbuf-16MiB.ipynb) |
| 16 MiB   | pydiode; redundancy=2 | UDP.c         | [pydiode-2-default-recbuf-16MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-16MiB/pydiode-2-default-recbuf-16MiB.ipynb) |
| 16 MiB   | pydiode; redundancy=2 | dd_udp.c      | [pydiode-2-dd_udp-recbuf-16MiB.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-16MiB/pydiode-2-dd_udp-recbuf-16MiB.ipynb) |


---


### Test results for MTU=9194 bytes and varying UDP receiver socket buffer

| Buffer size | Tool                  | Kernel module | Notebook |
| ---:     | ---                   | :---:         | ---      |
| 208 KiB  | Netcat                | UDP.c         | [NC-default-recbuf-208KiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuff-default/NC-default-recbuf-208KiB-mtu9194.ipynb) |
| 208 KiB  | Netcat                | dd_udp.c      | [NC-dd_udp-recbuf-208KiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuff-default/NC-dd_udp-recbuf-208KiB-mtu9194.ipynb) |
| 208 KiB  | pydiode; redundancy=1 | UDP.c         | [pydiode-1-default-recbuf-208KiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuff-default/pydiode-1-default-recbuf-208KiB-mtu9194.ipynb) |
| 208 KiB  | pydiode; redundancy=1 | dd_udp.c      | [pydiode-1-dd_udp-recbuf-208KiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuff-default/pydiode-1-dd_udp-recbuf-208KiB-mtu9194.ipynb) |
| 208 KiB  | pydiode; redundancy=2 | UDP.c         | [pydiode-2-default-recbuf-208KiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuff-default/pydiode-2-default-recbuf-208KiB-mtu9194.ipynb) |
| 208 KiB  | pydiode; redundancy=2 | dd_udp.c      | [pydiode-2-dd_udp-recbuf-208KiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuff-default/pydiode-2-dd_udp-recbuf-208KiB-mtu9194.ipynb) |
| 1 MiB    | Netcat                | UDP.c         | [NC-default-recbuf-1MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-01MiB/NC-default-recbuf-1MiB-mtu9194.ipynb) |
| 1 MiB    | Netcat                | dd_udp.c      | [NC-dd_udp-recbuf-1MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-01MiB/NC-dd_udp-recbuf-1MiB-mtu9194.ipynb) |
| 1 MiB    | pydiode; redundancy=1 | UDP.c         | [pydiode-1-default-recbuf-1MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-01MiB/pydiode-1-default-recbuf-1MiB-mtu9194.ipynb) |
| 1 MiB    | pydiode; redundancy=1 | dd_udp.c      | [pydiode-1-dd_udp-recbuf-1MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-01MiB/pydiode-1-dd_udp-recbuf-1MiB-mtu9194.ipynb) |
| 1 MiB    | pydiode; redundancy=2 | UDP.c         | [pydiode-2-default-recbuf-1MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-01MiB/pydiode-2-default-recbuf-1MiB-mtu9194.ipynb) |
| 1 MiB    | pydiode; redundancy=2 | dd_udp.c      | [pydiode-2-dd_udp-recbuf-1MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-01MiB/pydiode-2-dd_udp-recbuf-1MiB-mtu9194.ipynb) |
| 2 MiB    | Netcat                | UDP.c         | [NC-default-recbuf-2MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-02MiB/NC-default-recbuf-2MiB-mtu9194.ipynb) |
| 2 MiB    | Netcat                | dd_udp.c      | [NC-dd_udp-recbuf-2MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-02MiB/NC-dd_udp-recbuf-2MiB-mtu9194.ipynb) |
| 2 MiB    | pydiode; redundancy=1 | UDP.c         | [pydiode-1-default-recbuf-2MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-02MiB/pydiode-1-default-recbuf-2MiB-mtu9194.ipynb) |
| 2 MiB    | pydiode; redundancy=1 | dd_udp.c      | [pydiode-1-dd_udp-recbuf-2MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-02MiB/pydiode-1-dd_udp-recbuf-2MiB-mtu9194.ipynb) |
| 2 MiB    | pydiode; redundancy=2 | UDP.c         | [pydiode-2-default-recbuf-2MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-02MiB/pydiode-2-default-recbuf-2MiB-mtu9194.ipynb) |
| 2 MiB    | pydiode; redundancy=2 | dd_udp.c      | [pydiode-2-dd_udp-recbuf-2MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-02MiB/pydiode-2-dd_udp-recbuf-2MiB-mtu9194.ipynb) |
| 4 MiB    | Netcat                | UDP.c         | [NC-default-recbuf-4MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-04MiB/NC-default-recbuf-4MiB-mtu9194.ipynb) |
| 4 MiB    | Netcat                | dd_udp.c      | [NC-dd_udp-recbuf-4MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-04MiB/NC-dd_udp-recbuf-4MiB-mtu9194.ipynb) |
| 4 MiB    | pydiode; redundancy=1 | UDP.c         | [pydiode-1-default-recbuf-4MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-04MiB/pydiode-1-default-recbuf-4MiB-mtu9194.ipynb) |
| 4 MiB    | pydiode; redundancy=1 | dd_udp.c      | [pydiode-1-dd_udp-recbuf-4MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-04MiB/pydiode-1-dd_udp-recbuf-4MiB-mtu9194.ipynb) |
| 4 MiB    | pydiode; redundancy=2 | UDP.c         | [pydiode-2-default-recbuf-4MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-04MiB/pydiode-2-default-recbuf-4MiB-mtu9194.ipynb) |
| 4 MiB    | pydiode; redundancy=2 | dd_udp.c      | [pydiode-2-dd_udp-recbuf-4MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-04MiB/pydiode-2-dd_udp-recbuf-4MiB-mtu9194.ipynb) |
| 8 MiB    | Netcat                | UDP.c         | [NC-default-recbuf-8MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-08MiB/NC-default-recbuf-8MiB-mtu9194.ipynb) |
| 8 MiB    | Netcat                | dd_udp.c      | [NC-dd_udp-recbuf-8MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-08MiB/NC-dd_udp-recbuf-8MiB-mtu9194.ipynb) |
| 8 MiB    | pydiode; redundancy=1 | UDP.c         | [pydiode-1-default-recbuf-8MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-08MiB/pydiode-1-default-recbuf-8MiB-mtu9194.ipynb) |
| 8 MiB    | pydiode; redundancy=1 | dd_udp.c      | [pydiode-1-dd_udp-recbuf-8MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-08MiB/pydiode-1-dd_udp-recbuf-8MiB-mtu9194.ipynb) |
| 8 MiB    | pydiode; redundancy=2 | UDP.c         | [pydiode-2-default-recbuf-8MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-08MiB/pydiode-2-default-recbuf-8MiB-mtu9194.ipynb) |
| 8 MiB    | pydiode; redundancy=2 | dd_udp.c      | [pydiode-2-dd_udp-recbuf-8MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-08MiB/pydiode-2-dd_udp-recbuf-8MiB-mtu9194.ipynb) |
| 16 MiB   | Netcat                | UDP.c         | [NC-default-recbuf-16MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-16MiB/NC-default-recbuf-16MiB-mtu9194.ipynb) |
| 16 MiB   | Netcat                | dd_udp.c      | [NC-dd_udp-recbuf-16MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-16MiB/NC-dd_udp-recbuf-16MiB-mtu9194.ipynb) |
| 16 MiB   | pydiode; redundancy=1 | UDP.c         | [pydiode-1-default-recbuf-16MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-16MiB/pydiode-1-default-recbuf-16MiB-mtu9194.ipynb) |
| 16 MiB   | pydiode; redundancy=1 | dd_udp.c      | [pydiode-1-dd_udp-recbuf-16MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-16MiB/pydiode-1-dd_udp-recbuf-16MiB-mtu9194.ipynb) |
| 16 MiB   | pydiode; redundancy=2 | UDP.c         | [pydiode-2-default-recbuf-16MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-16MiB/pydiode-2-default-recbuf-16MiB-mtu9194.ipynb) |
| 16 MiB   | pydiode; redundancy=2 | dd_udp.c      | [pydiode-2-dd_udp-recbuf-16MiB-mtu9194.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-16MiB/pydiode-2-dd_udp-recbuf-16MiB-mtu9194.ipynb) |


---


### Test results for Data segment size of 9166 bytes, MTU=9194 bytes, and varying UDP receiver socket buffer

| Buffer size | Tool                  | Kernel module | Notebook |
| ---:     | ---                   | :---:         | ---      |
| 208 KiB  | pydiode; redundancy=1 | UDP.c         | [pydiode-1-default-recbuf-208KiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuff-default/pydiode-1-default-recbuf-208KiB-mtu9194-9166.ipynb) |
| 208 KiB  | pydiode; redundancy=1 | dd_udp.c      | [pydiode-1-dd_udp-recbuf-208KiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuff-default/pydiode-1-dd_udp-recbuf-208KiB-mtu9194-9166.ipynb) |
| 208 KiB  | pydiode; redundancy=2 | UDP.c         | [pydiode-2-default-recbuf-208KiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuff-default/pydiode-2-default-recbuf-208KiB-mtu9194-9166.ipynb) |
| 208 KiB  | pydiode; redundancy=2 | dd_udp.c      | [pydiode-2-dd_udp-recbuf-208KiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuff-default/pydiode-2-dd_udp-recbuf-208KiB-mtu9194-9166.ipynb) |
| 1 MiB    | pydiode; redundancy=1 | UDP.c         | [pydiode-1-default-recbuf-1MiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-01MiB/pydiode-1-default-recbuf-1MiB-mtu9194-9166.ipynb) |
| 1 MiB    | pydiode; redundancy=1 | dd_udp.c      | [pydiode-1-dd_udp-recbuf-1MiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-01MiB/pydiode-1-dd_udp-recbuf-1MiB-mtu9194-9166.ipynb) |
| 1 MiB    | pydiode; redundancy=2 | UDP.c         | [pydiode-2-default-recbuf-1MiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-01MiB/pydiode-2-default-recbuf-1MiB-mtu9194-9166.ipynb) |
| 1 MiB    | pydiode; redundancy=2 | dd_udp.c      | [pydiode-2-dd_udp-recbuf-1MiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-01MiB/pydiode-2-dd_udp-recbuf-1MiB-mtu9194-9166.ipynb) |
| 2 MiB    | pydiode; redundancy=1 | UDP.c         | [pydiode-1-default-recbuf-2MiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-02MiB/pydiode-1-default-recbuf-2MiB-mtu9194-9166.ipynb) |
| 2 MiB    | pydiode; redundancy=1 | dd_udp.c      | [pydiode-1-dd_udp-recbuf-2MiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-02MiB/pydiode-1-dd_udp-recbuf-2MiB-mtu9194-9166.ipynb) |
| 2 MiB    | pydiode; redundancy=2 | UDP.c         | [pydiode-2-default-recbuf-2MiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-02MiB/pydiode-2-default-recbuf-2MiB-mtu9194-9166.ipynb) |
| 2 MiB    | pydiode; redundancy=2 | dd_udp.c      | [pydiode-2-dd_udp-recbuf-2MiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-02MiB/pydiode-2-dd_udp-recbuf-2MiB-mtu9194-9166.ipynb) |
| 4 MiB    | pydiode; redundancy=1 | UDP.c         | [pydiode-1-default-recbuf-4MiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-04MiB/pydiode-1-default-recbuf-4MiB-mtu9194-9166.ipynb) |
| 4 MiB    | pydiode; redundancy=1 | dd_udp.c      | [pydiode-1-dd_udp-recbuf-4MiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-04MiB/pydiode-1-dd_udp-recbuf-4MiB-mtu9194-9166.ipynb) |
| 4 MiB    | pydiode; redundancy=2 | UDP.c         | [pydiode-2-default-recbuf-4MiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-04MiB/pydiode-2-default-recbuf-4MiB-mtu9194-9166.ipynb) |
| 4 MiB    | pydiode; redundancy=2 | dd_udp.c      | [pydiode-2-dd_udp-recbuf-4MiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-04MiB/pydiode-2-dd_udp-recbuf-4MiB-mtu9194-9166.ipynb) |
| 8 MiB    | pydiode; redundancy=1 | UDP.c         | [pydiode-1-default-recbuf-8MiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-08MiB/pydiode-1-default-recbuf-8MiB-mtu9194-9166.ipynb) |
| 8 MiB    | pydiode; redundancy=1 | dd_udp.c      | [pydiode-1-dd_udp-recbuf-8MiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-08MiB/pydiode-1-dd_udp-recbuf-8MiB-mtu9194-9166.ipynb) |
| 8 MiB    | pydiode; redundancy=2 | UDP.c         | [pydiode-2-default-recbuf-8MiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-08MiB/pydiode-2-default-recbuf-8MiB-mtu9194-9166.ipynb) |
| 8 MiB    | pydiode; redundancy=2 | dd_udp.c      | [pydiode-2-dd_udp-recbuf-8MiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-08MiB/pydiode-2-dd_udp-recbuf-8MiB-mtu9194-9166.ipynb) |
| 16 MiB   | pydiode; redundancy=1 | UDP.c         | [pydiode-1-default-recbuf-16MiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-16MiB/pydiode-1-default-recbuf-16MiB-mtu9194-9166.ipynb) |
| 16 MiB   | pydiode; redundancy=1 | dd_udp.c      | [pydiode-1-dd_udp-recbuf-16MiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-16MiB/pydiode-1-dd_udp-recbuf-16MiB-mtu9194-9166.ipynb) |
| 16 MiB   | pydiode; redundancy=2 | UDP.c         | [pydiode-2-default-recbuf-16MiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-16MiB/pydiode-2-default-recbuf-16MiB-mtu9194-9166.ipynb) |
| 16 MiB   | pydiode; redundancy=2 | dd_udp.c      | [pydiode-2-dd_udp-recbuf-16MiB-mtu9194-9166.ipynb](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Notebooks/recbuf-16MiB/pydiode-2-dd_udp-recbuf-16MiB-mtu9194-9166.ipynb) |

