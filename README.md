<!-- pandoc -V geometry:margin=1cm -V fontsize=12pt -V fontfamily=utopia README.md -o README.pdf -->

# RIIM SLIP example 

## Description
This is an intermediate complex example reflecting a simple real world scenario. The scenario is as follows:

---

   You want to create a system consisting of a few nodes logging the temperature at different locations. The system uses CoAP to send and receive data to/from a border router connected to an edge computer. The edge computer is a Raspberry Pi 3 running the Node RED application. You need to use IPv6 all the way.

---

## Requirements
|                   |                   |
| ----------------- | ----------------- |
| Operating system  | Raspberry Pi OS: 5.10.17-v7+   |
| Computer/Board    | Raspberry Pi 3    |

## Downloading
Download the source, either by cloning the repository like this:

`
git clone https://github.com/RCfesk/RIIM_Slip.git
`


...or downloading the zip file provided here:
[https://github.com/RCfesk/RIIM_Slip/blob/master/Packages/RIIM_Slip.zip]

## Installation
If you downloaded the zip-file, unzip it first.

Then enter the **riim_slip** folder and run the install script

`
./install.sh
`


## Full Documentation
Please see the documentation located here:
[https://github.com/RCfesk/RIIM_Slip/blob/master/Doc/build/html/index.html]
