Walkthrough / Quickstart
========================

To get the example up and running without any modifications, you can follow this walkthorugh

#. Set up the Edge Computer as described in the vendors documentation (for instance : `<https://www.raspberrypi.org/>`_
#. Open a terminal and navigate to the RIIM SLIP Example folder
#. Execute the **./install.sh** script
   - This installs all required dependencies
#. Run the **./start.sh** script
#. Follow the guide for setting up Node RED described in the *Node RED Setup* chapter
#. When the script ends, go to this address using a browser in the raspberry pi :  `<http://localhost:1880/>`_ . If not running the browser from the Raspberry pi, please see the troubleshooting chapter to find the IP address of your edge computer.
#. You are up and running. Now you can observe the data, make modifications and play around.


How to observe the output
-------------------------
The output is default printed to the console. The output will be printed in the same console as you ran **./start.sh**. You can also enable output in Node-RED itself by enabling the green **msg** nodes and selecting **Debug messages**. The debug messages are very detailed, so it is recommended to use the console.


Modifications and customization
-------------------------------

See the **./install.sh** script for details. It is well documented and should give you a good explanation on what is going on

