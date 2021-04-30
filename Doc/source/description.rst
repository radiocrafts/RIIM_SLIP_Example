Acronyms
========

=========== ===========================================
UART        Universal Asynchronous Receiver Transmitter
SLIP        Serial Line IP
=========== ===========================================

Description
===========
This is an intermediate complex example reflecting a simple real world scenario. The scanario is as follows:

   You want to create a system consisting of a few nodes logging the temperature at different locations. The system uses CoAP to send and receive data to/from a border router connected to an edge computer. The edge computer is a Raspberry Pi 3 running the Node RED application. You need to use IPv6 all the way.

   The main challenges and tasks are therefore these:

   - The addresses of the nodes are not known beforehand. So after deployment this info needs to be gathered automatically.
   - The edge computer needs to be set up to support IPv6 routing, connect to the border router using SLIP and connect the network to the Node RED application
   - The ICI applications for the Border Router and the Mesh Routers needs to be developed
   - An application (flow) for the Node RED application needs to be developed

This example provides a possible solution to these challenges and tasks


System Overview
---------------
This image shows the system. The dashed grey parts are optinal, and not part of this example. They probably would, however, be in a real deployment.

.. mermaid::

   graph LR
      idInt(Internet) --- idRPI(edge computer)
      idRPI(edge computer) -- SLIP --- idBR(BorderRouter)
      idBR(BorderRouter) -- RF --- idMR1(MeshRouter)
      idBR(BorderRouter) -- RF --- idMR2(MeshRouter)
      idMR1(MeshRouter) -- RF --- idMR3(MeshRouter)
      idMR1(MeshRouter) -- RF --- idMR4(MeshRouter)
      
      style idInt fill:#aaa,stroke:#888,stroke-width:2px,color:#fff,stroke-dasharray: 3 3
      style idMR2 fill:#aaa,stroke:#888,stroke-width:2px,color:#fff,stroke-dasharray: 3 3
      style idMR3 fill:#aaa,stroke:#888,stroke-width:2px,color:#fff,stroke-dasharray: 3 3
      style idMR4 fill:#aaa,stroke:#888,stroke-width:2px,color:#fff,stroke-dasharray: 3 3

A CoAP server/client runs on an edge computer. The edge computer runs the Node RED application to connect and implement networking. The edge computer communicates with a RIIM Border Router using SLIP over UART, and is able to talk to all RIIM nodes using IPv6 natively. All RIIM nodes also run CoAP server/clients.



Topics not covered in this example
----------------------------------
These topics are not covered in this example, but could be relevant in a real world deployment

- Installation of operating system (See `<https://www.raspberrypi.org/software/operating-systems/>`_
- How to customize (low level) Linux network setup such as routing, proxying, firewalls etc.
- Migration to other operating systems, hardware or Linux distributions
- Security policies, such as parts running with administrator privilegies, Node Red keys, DTLS etc.
- Containerizations, virtualizations, Python environments
- edge computer application auto startup on boot (See `<https://nodered.org/docs/getting-started/raspberrypi>`_


Edge Computer
-------------

This example uses a Raspberry Pi 3 running Raspberry Pi OS as an example. Migration to other single board computers, other Linux distributions or even PCs are outside the scope of this example. However, if keeping to mainstream hardware and Linux-based operating systems, migration should be fairly simple.


RIIM network nodes
------------------

There are two ICI applications provided:

- Border Router application
   - Connects via SLIP using UART
   - Sets up a CoAP resource called **"BRData"** that is accessible from all nodes and SLIP
   - BRData can respond to CoAP GET and CoAP PUT, to read/write an IPv6 address
   - This address is used to send periodic CoAP messages from the BR
   - If no IPv6 address is set in **BRData** , the node periodically send its IPv6 address to coap://[fd00::1:1234]/CommData
   - This is used for commisioning, as the server gets to know the address of the node

- Mesh Router application
   - Sets up a CoAP resource called **"MRData"** that is accessible from BR and everything the BR is connected to
   - BRData can respond to CoAP GET and CoAP PUT, to read/write an IPv6 address
   - This address is used to send periodic CoAP messages from the MR
   - The application also prints out the source and destination address on UART


Node Red Server
---------------

In this example, the server runs Node Red, a popular programming tool for connecting hardware, services and APIs. 
