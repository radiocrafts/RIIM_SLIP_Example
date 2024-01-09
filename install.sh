#!/bin/bash

echo " "
echo "************************************************************"
echo "It is recommended that you read the documentation before"
echo "you continue with the installation. It is located in"
echo "./Doc/build/html/index.html . Do you want to open it now?"
echo "(Requires web browser)"
echo "Press [y/n] and <ENTER> : "
read ViewDoc

if [ "$ViewDoc" == "y" ]
then
    xdg-open ./docs/build/html/index.html &
fi
# This script assumes you need sudo to execute apt install
# It does not check for already existing installations


echo " "
echo "************************************************************"
echo "Installing required packages"
echo " We use sudo for apt install, so your password may be required"
echo " during installation"
echo "Press <ENTER> to continue"
read

# Mandatory packages
sudo apt install build-essential
sudo apt install git
sudo apt install python3 python3-pip
sudo apt install xdg-utils

# Python packages
pip3 install --user pycryptodomex pyserial sphinxcontrib-mermaid sphinx-rtd-theme

# Generate documentation
pushd ./Doc
make html
popd


echo " "
echo "************************************************************"
echo "Do you also want to install the recommended optional packages (wireshark, microcom, tcpdump)"
echo "Press [y/n] and <ENTER> : "
read InstallOptional

# Optional packages
if [ "$InstallOptional" == "y" ]
then
    sudo apt install wireshark
    sudo apt install microcom
    sudo apt install tcpdump
fi

echo " "
echo "************************************************************"
echo "Is your system 32 or 64 bit? If unsure, try 32 bit first"
echo "1. 32 bit"
echo "2. 64 bit"
echo "Select [1,2] and press <ENTER> : "
read SystemType

if [ $SystemType -eq 1 ] 
then
    echo "Using 32 bit"
    cp Tools/Tunslip_Binaries/32-bit/tunslip6 Tools/
else
    echo "Using 64 bit"
    cp Tools/Tunslip_Binaries/64-bit/tunslip6 Tools/
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

