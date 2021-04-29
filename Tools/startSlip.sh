#!/usr/bin/env bash

# Kill other running instances
sudo pkill tunslip6

NetworkDevice=eth0
#SerialDevice=/dev/ttyUSB0
SerialDevice=/dev/serial0
TUNAddr=1:1234


#IPAddr_Full=$(ip -6 addr | grep "inet6 2" | grep "scope global" | awk '{print $2}')
IPAddr_Full="fd00:0:0:0:0:0:1:1234"
IPAddr=$(echo $IPAddr_Full | awk -F/ '{print $1}')
Prefix=$(echo $IPAddr | awk -F: '{print $1 ":" $2 ":" $3 ":" $4}')

echo $IPAddr_Full
echo $IPAddr
echo $Prefix

# Enable forwarding and proxying
sudo sysctl net.ipv6.conf.all.forwarding=1
sudo sysctl net.ipv6.conf.all.proxy_ndp=1

# Start the tunslip tool
sudo ./tunslip6 -v -s $SerialDevice $Prefix::$TUNAddr/64 &

# Generate the radvd configuration file
read -r -d '' VAR << EOF

   interface $NetworkDevice
   {
        AdvSendAdvert on;
        MaxRtrAdvInterval 30;
        AdvLinkMTU 1280;

        prefix $Prefix::0/64
        {
                AdvOnLink on;
                AdvAutonomous on;
        };

   };
EOF

echo "$VAR" > /etc/radvd.conf

# Start radvd
sudo radvd

