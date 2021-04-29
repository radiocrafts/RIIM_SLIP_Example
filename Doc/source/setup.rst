System Setup
============

Linux Machine Setup
-------------------

*Note:* Running the **./Tools/Setup.sh** script helps you install all prerquisites and set up the Linux Machine (RPI3)


Mandatory Prerequisites
-----------------------

radvd
+++++
radvd is a tool for routing IPv6 traffic. It can be installed like this
.. code-block::

    sudo apt install radvd

python3
+++++++
Python is an interpreted programming language. It can be installed like this
.. code-block::

    sudo apt install python3

Python packages
+++++++++++++++
Python needs a few packages that are used by the tools provided. These can be installed like this
.. code-block::

    pip3 install --user pycryptodomex pyserial

node-red
++++++++
Node Red is a programming tool for connecting hardware, services and APIs. It can either be installed using the package manager like this (Not recommended, but easier):
.. code-block::

    sudo apt install Node-RED

Or it can be installed using the install script on the official page `<https://nodered.org/docs/getting-started/raspberrypi>`_ (Recommended, but a little harder)


Optional Prerequisites
----------------------

wireshark
+++++++++
Wireshark is a tool for anayzing network traffic. It is useful for analyzing and debugging problems related to network traffic. It it can be installed like this
.. code-block::

    sudo apt install wireshark


Microcom
++++++++
Microcom is a simple terminal program that can be used for interfacing UART based serial interfaces. It can be installed like this
.. code-block::

    sudo apt install microcom


ARM compiler tools
++++++++++++++++++

arm-none-eabi-gcc and related tools are tools for compiling the ICI applications. You need this to complie your own ICI applications. There are two ways to install it. The simplest is to use the packet manager
.. code-block::

    sudo apt install binutils-arm-none-eabi gcc-arm-none-eabi

Or it can be installed using a specific version from `<https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads>`_


Network Setup
-------------

In general network setup on this level can be complicated. Radiocrafts provide a setup script that sets up all the essentials for the example to work, and leaves out the unneccesary bits. In combination with the Node Red server, this should be sufficient for your application to connect to whatever online server you are using.

The script uses a precompiled SLIP/TUN driver. This driver is responsible for connecting to the UART and map it to a virtual network device (TUN). This TUN device can in turn be used like most other network devices.


