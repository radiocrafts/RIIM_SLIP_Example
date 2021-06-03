#!/bin/bash
pushd Tools

echo "Starting example"
echo "Do you want to upload the platforms to the boards [y/n]?"
echo "This is only neccesary if not already uploaded."
read UploadPlatforms
echo "Do you want to upload ICI applications to the boards [y/n]?"
echo "This is only neccesary if not already uploaded."
read UploadICI

echo "What is the serial port of the Border Router? (E.g. /dev/ttyUSB0 - See documentation - troubleshooting for help)"
read BRPort

if [ $UploadICI == "y" ] || [ $UploadPlatforms == "y" ]
then
    if [ $UploadPlatforms == "y" ]
    then
    python3 ./rc18xx_bootloader_utility/rc188x_bootloader_utility.py load-image -t 100 -p $BRPort -f ../Platforms/BR_Platform.bin
    fi

    if [ $UploadICI == "y" ]
    then
    python3 ./rc18xx_bootloader_utility/rc188x_bootloader_utility.py load-image -t 100 -p $BRPort -f ../ICI_Applications/Example_SLIP/Output/BR.bin
    fi

    echo "What is the port of the Mesh Router? (E.g. /dev/ttyUSB1 - See documentation - troubleshooting for help)"
    read MRPort
    if [ $UploadPlatforms == "y" ]
    then
    python3 ./rc18xx_bootloader_utility/rc188x_bootloader_utility.py load-image -t 100 -p $MRPort -f ../Platforms/MR_Platform.bin
    fi

    if [ $UploadICI == "y" ]
    then
    python3 ./rc18xx_bootloader_utility/rc188x_bootloader_utility.py load-image -t 100 -p $MRPort -f ../ICI_Applications/Example_SLIP/Output/MR.bin
    fi
fi

echo "Starting SLIP"
sudo ./startSlip.sh $BRPort

# SLIP takes some time to start
sleep 5
echo " "
echo "************************************************************"
echo "We will now start Node Red. After it has started, you can"
echo "access it using your browser. See the documentation to find"
echo "out how to determine your IP address."
echo "However, here is a list of possible addresses:"

ip a | grep inet

echo " "
echo "Press RESET on boards and press <ENTER>"
read something

popd 

echo "Starting Node Red"
node-red-pi --max-old-space-size=256


