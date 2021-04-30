#!/bin/bash

# This script assumes you need sudo to execute apt install
# It does not check for already existing installations

echo " "
echo "************************************************************"
echo "This script will install all mandatory packages"
echo "Do you also want to install the recommended optional packages (wireshark, microcom, tcpdump)"
echo "Press [y/n] and <ENTER> : "
read InstallOptional

# Mandatory packages
sudo apt install build-essential
sudo apt install git
sudo apt install radvd
sudo apt install python3 pyhton3-pip

# Python packages
pip3 install --user pycryptodomex pyserial

# Optional packages
if [ "$InstallOptional" == "y" ]
then
    sudo apt install wireshark
    sudo apt install microcom
    sudo apt install tcpdump
fi

# Node Red is special
echo " "
echo "************************************************************"
echo "Node Red must be installed. You can install it:"
echo "1. using the package manager (easier), or"
echo "2. The install script on nodered.org (recommended)"
echo "Select [1,2] and press <ENTER> : " 
read InstallType

if [ $InstallType -eq 1 ] 
then
    echo "Using package manager to install Node Red"
    sudo apt install nodered
else
    echo "Please go to https://nodered.org/docs/getting-started/raspberrypi for instructions on how to install Node Red"
fi

