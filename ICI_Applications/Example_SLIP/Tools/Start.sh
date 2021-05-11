#!/bin/bash

echo "Starting example"
echo "Do you want to upload ICI applications to the boards [y/n]?"
read UploadICI

if [ $UploadICI == "y" ]
    python3 ./Tools/rc1882_bootloader_utility/rc188x_bootloader_utility.py
then
fi

echo "Starting Node Red"
node-red-start

echo " "
echo "************************************************************"
echo "You can now access Node Red using your browser."
echo "Open your browser and go to the address ********"
