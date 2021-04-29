#!/bin/bash

echo "Do you want to upload ICI application to Border Router or Mesh Router [b/m] : "
read BRMR

if [ $BRMR == "b" ]
then
    echo "Which port is the Border Router connected to (e.g. /dev/ttyUSB0) : "
    BoardFile="./Output/BR.bin"
else
    echo "Which port is the Mesh Router connected to (e.g. /dev/ttyUSB0) : "
    BoardFile="./Output/MR.bin"
fi

read Port
python3 ./Tools/rc1882_bootloader_utility/rc188x_bootloader_utility.py load-image -p $Port -f $BoardFile -t 100
