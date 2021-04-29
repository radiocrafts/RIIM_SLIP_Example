<!-- pandoc -V geometry:margin=1cm -V fontsize=12pt -V fontfamily=utopia README.md -o README.pdf -->

# RIIM SLIP example

- [RIIM SLIP example](#riim-slip-example)
  - [Description](#description)
    - [RIIM network nodes](#riim-network-nodes)
    - [Linux machine](#linux-machine)
      - [Prerequisites](#prerequisites)
      - [System Setup](#system-setup)
      - [Network setup](#network-setup)
      - [Node Red Server](#node-red-server)
  - [Topics not covered in this example](#topics-not-covered-in-this-example)
  - [Walkthrough](#walkthrough)
    - [Setup](#setup)
    - [Start example](#start-example)
    - [](#)

## Description
This is an intermediate complex example reflecting a simple real world scenario. 

### RIIM network nodes
There are two applications provided:
- Border Router application
    - Connects via SLIP using UART
    - Sets up a CoAP resource called **"BRData"** that is accessible from all nodes and SLIP
        - BRData can respond to CoAP GET and CoAP PUT, to read/write an IPv6 address
        - This address is used to send periodic CoAP messages from the BR
    - If no IPv6 address is set in **BRData** , the node periodically send its IPv6 address to coap://[fd56::1:0001]/CommData
        - This is used for commisioning, as the server gets to know the address of the node

- Mesh Router application
   - Sets up a CoAP resource called **"MRData"** that is accessible from BR and everything the BR is connected to
   - BRData can respond to CoAP GET and CoAP PUT, to read/write an IPv6 address
   - This address is used to send periodic CoAP messages from the MR
   - The application also prints out the source and destination address on UART

### Linux machine
This example uses a Raspberry Pi 3 (RPI3) running Raspberry Pi OS as an example. Migration to other single board computers (SBCs), other Linux distributions or even PCs are outside the scope of this example. However, if keeping to mainstream hardware and Linux-based operating systems, migration should be fairly simple.

#### Prerequisites
*All prerequisites are installed when you execute the **Setup.sh** script*
You need the following installed on the RPI3:
- node-red - The "IoT server"
- radvd
- python3

Also Radiocrafts recommend these tools for development and debugging:
- wireshark - To analyze network traffic
- microcom - A simple terminal program
- arm-none-eabi-gcc and related tools - Compiler tools for compiling the ICI application

#### System Setup

#### Network setup
In general network setup on this level can be complicated. Radiocrafts provide a setup script that sets up all the essentials for the example to work, and leaves out the unneccesary bits. In combination with the Node Red server, this should be sufficient for your application to connect to whatever online server you are using.

The script uses a precompiled SLIP/TUN driver. This driver is responsible for connecting to the UART and map it to a virtual network device (TUN). This TUN device can in turn be used like most other network devices.

#### Node Red Server
In this example, the server runs Node Red, a popular programming tool for connecting hardware, services and APIs. 

These applications are part of the RIIM_IPv6_Slip example which demonstrates a full data flow/control of a RIIM network using IPv6 and SLIP.

## Topics not covered in this example
- How to customize (low level) Linux network setup such as routing, proxying, firewalls etc.
- Migration to other operating systems, hardware or Linux distributions
- Security policies, such as parts running with administrator privilegies, Node Red keys, DTLS etc.

## Walkthrough

### Setup
- Set up the computer as described in the user manual
- Execute the **Setup.sh** script

### Start example
- Execute the **Start.sh** script

### 
