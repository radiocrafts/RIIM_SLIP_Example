Troubleshooting
===============

I'm not able to access the serial port
--------------------------------------
Your user must be part of the **dialout** group. Use this command to fix it
.. code-block::

    sudo adduser $USER dialout

You need to re-login (or even reboot) for the changes to take effect