<!-- pandoc -V geometry:margin=1cm -V fontsize=12pt -V fontfamily=utopia README.md -o README.pdf -->

# RIIM SLIP example

## Description
This is an intermediate complex example reflecting a simple real world scenario. 
There are two applications provided:
- Border Router application
   - Connects via SLIP using UART
   - Sets ut a CoAP resource called **"BRData"** that is accessible from all nodes and SLIP
   - BRData can respond to CoAP GET and CoAP PUT, to read/write an IPv6 address
   - This address is used to send periodic CoAP messages from the BR

- Mesh Router application
   - Sets ut a CoAP resource called **"MRData"** that is accessible from BR and everything the BR is connected to
   - BRData can respond to CoAP GET and CoAP PUT, to read/write an IPv6 address
   - This address is used to send periodic CoAP messages from the MR
   - The application also prints out the source and destination address on UART

These applications are part of the RIIM_IPv6_Slip example which demonstrates a full data flow/control of a RIIM network using IPv6 and SLIP.

## To use this example:

### Compile and upload
- Set up the computer as described in the user manual
- Use the **Compile_And_Upload** script or use MAKE manually to generate and upload the images

###
