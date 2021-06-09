Troubleshooting
===============

I'm not able to access the serial port
--------------------------------------
Your user must be part of the **dialout** group. Use this command to fix it

.. code-block:: bash

    sudo adduser $USER dialout

You need to re-login (or even reboot) for the changes to take effect


How do I find the IP address of the Edge Computer
-------------------------------------------------
Execute the following command

.. code-block:: bash

    ip a

This will list all addresses associated with your system. For example:

.. code-block:: bash
    :emphasize-lines: 3,5

    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
        link/ether XX:XX:XX:XX:XX:XX brd ff:ff:ff:ff:ff:ff
        inet XXX.XXX.XXX.XXX/24
        valid_lft 2653sec preferred_lft 2024sec
        inet6 XXXX::XXXX:XXXX:XXXX:XXXX/64
        valid_lft forever preferred_lft forever


For accessing Node RED, you can use either the IPv4 (specified by **inet** above) or IPv6 address (specified by **inet6** above) of the board.


How do I find the serial port used for the Border Router
--------------------------------------------------------

In Linux, the drivers for the USB-to-UART IC (FTDI FT-series) is built into the kernel. When a new board is connected, a new device will automatically appear in the **/dev/** folder. The name will be ttyUSB followed by a number, which start at zero for the first device enumerated. Therefore:

- The first device enumerated will get the device **/dev/ttyUSB0**
- The next will get the device **/dev/ttyUSB1**
- ....and so on.


How do I use tunslip6 on my particular system
---------------------------------------------
tunslip6 is provided in source form as tunslip6.c located in the Tools folder. Adaption of this to any specific platform is not supported by Radiocrafts directly. But, as the source code is available, you may choose to adapt and compile it yourself.