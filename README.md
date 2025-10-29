# DataDiodesAndPacketLoss

This repo contains all files related to my Master's thesis: <b>Limiting Packet Loss on a Strictly Unidirectional Physical Data Diode</b>.

## Contents
- [Thesis: Limiting Packet Loss on a Strictly Unidirectional Physical Data Diode](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/Thesis-GJdenBesten-20251025.pdf)
- [Linux dd_udp.c kernel module](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/tree/main/dd_udp-module)
- [Index to Jupyter Notebooks and Test results](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/blob/main/IndexNotebooksAndTestResults.md)
- [Linux/Bash scripts](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/tree/main/Scripts)
- [Python test scripts](https://github.com/Gert-Jan1966/DataDiodesAndPacketLoss/tree/main/Testscripts)

&nbsp;&nbsp;&nbsp;&nbsp;

<center>
  <img src="https://raw.githubusercontent.com/Gert-Jan1966/DataDiodesAndPacketLoss/refs/heads/main/OneDoesNotSimply-DD.jpg" alt="Meme" style="width:360px;"/>
</center>

&nbsp;&nbsp;&nbsp;&nbsp;

## Summary
Physical data diodes are a cybersecurity measure that enable unidirectional data transfer between physically separated networks. This one-way communication prevents information from leaking from the destination network back to the source network. Although various commercial solutions are available, relatively few academic publications address data diodes.

One of the main challenges of unidirectional data transfer is the potential loss of transmitted data, also known as packet loss.
This study aims to contribute to the existing body of research by laying the groundwork for further investigation into where and when packet loss occurs and how it can be mitigated. This thesis describes an enhancement to the Linux UDP.c kernel module, dd_udp.c, developed to handle UDP traffic within data diodes more efficiently. In addition, measurement points within the Linux networking stack are selected and other measurement points are implemented in this alternative module, providing greater insight into UDP data transmission.

This study makes use of a simple data diode test setup that is described both on an informative GitHub website and in an academic publication from 2023. This setup makes use of a single workstation with two network interfaces. Tests are conducted by sending files using Netcat and pydiode. The latter tool was introduced in the aforementioned 2023 publication. While Netcat allows for simple data transmission, pydiode enables the use of redundant data transmission. Additional tests are performed with increased UDP receiver socket buffer sizes, modified values for the MTU, and for modified data segment sizes that Netcat and pydiode attempt to send.

The results show that there are no consistent performance or efficiency differences between the two kernel modules. When testing the other factors, it is observed that increasing the UDP receiver socket buffer, when using pydiode, quickly leads to an efficiency of 100%, whereas this was not always the case in the 2023 publication. Variations in the other tested factors have little impact within the context of this test setup.

Recommendations for future research include modifying the dd_udp.c module for use on two separate workstations, thereby turning the module itself into a security measure; conducting test scenarios that more closely resemble real-life situations; experimenting with system settings on which the sender and receiver processes run; and, finally, developing a predictive model to minimize packet loss.

&nbsp;

October 2025 - G.J. den Besten

