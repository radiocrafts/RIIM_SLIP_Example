Description
===========
This is an intermediate complex example reflecting a simple real world scenario.

File Structure
--------------



System Overview
---------------
A CoAP server/client runs on an endge computer. This communicates with a RIIM Border Router using SLIP, and is able to talk to all RIIM nodes using IPv6 natively. All RIIM nodes also run CoAP server/clients.

Topics not covered in this example
----------------------------------
- Installation of core operating system on the RPI3
- How to customize (low level) Linux network setup such as routing, proxying, firewalls etc.
- Migration to other operating systems, hardware or Linux distributions
- Security policies, such as parts running with administrator privilegies, Node Red keys, DTLS etc.


Linux machine
-------------

This example uses a Raspberry Pi 3 (RPI3) running Raspberry Pi OS as an example. Migration to other single board computers (SBCs), other Linux distributions or even PCs are outside the scope of this example. However, if keeping to mainstream hardware and Linux-based operating systems, migration should be fairly simple.


RIIM network nodes
------------------

There are two ICI applications provided:

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
