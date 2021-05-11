System Setup
============

Linux Machine Setup
-------------------


Prerequisites
-------------


*Note:* All prerequisites are installed when you execute the **Setup.sh** script

You need the following installed on the RPI3:

- node-red - The "IoT server"
- radvd
- python3

Also Radiocrafts recommend these tools for development and debugging:

- wireshark - To analyze network traffic
- microcom - A simple terminal program
- arm-none-eabi-gcc and related tools - Compiler tools for compiling the ICI application


Network Setup
-------------

In general network setup on this level can be complicated. Radiocrafts provide a setup script that sets up all the essentials for the example to work, and leaves out the unneccesary bits. In combination with the Node Red server, this should be sufficient for your application to connect to whatever online server you are using.

The script uses a precompiled SLIP/TUN driver. This driver is responsible for connecting to the UART and map it to a virtual network device (TUN). This TUN device can in turn be used like most other network devices.


Node Red Server
---------------

In this example, the server runs Node Red, a popular programming tool for connecting hardware, services and APIs. 

These applications are part of the RIIM_IPv6_Slip example which demonstrates a full data flow/control of a RIIM network using IPv6 and SLIP.
