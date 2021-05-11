/*****************************************************************************
 * Copyright ©2021. Radiocrafts AS (Radiocrafts).  All Rights Reserved. 
 * Permission to use, copy, modify, and distribute this software and 
 * its documentation, without fee and without a signed licensing 
 * agreement, is hereby granted, provided that the above copyright 
 * notice, this paragraph and the following two paragraphs appear in 
 * all copies, modifications, and distributions.
 * 
 * IN NO EVENT SHALL RADIOCRFTS BE LIABLE TO ANY PARTY FOR DIRECT, 
 * INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING 
 * LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS 
 * DOCUMENTATION, EVEN IF RADIOCRAFTS HAS BEEN ADVISED OF THE 
 * POSSIBILITY OF SUCH DAMAGE. 
 * 
 * RADIOCRAFTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT 
 * NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND 
 * FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING 
 * DOCUMENTATION, IF ANY, PROVIDED HEREUNDER IS PROVIDED "AS IS". 
 * RADIOCRAFTS HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, 
 * UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
****************************************************************************/

/**
 @file
 @brief 
 @version 
 @date 
*/

#include "RIIM_UAPI.h"

static const uint32_t   timerPeriod=1000;
static uint8_t timerHandler;

//const IPAddr DestIP={.byte={0x20, 0x01, 0x46, 0x46, 0xf8, 0x86,0,0,0,0,0,0,0 ,0x01,0x12,0x34}};

IPAddr DestIP;
bool SendPeriodicCoAPMessage=false;

const uint8_t CoAP_ResourceName[]="BRData";
const uint8_t CoAP_DestinationCoAPResource[]="ServerData";
const uint8_t CoAP_TransmissionString[]="Hello, World!";

void UAPI_CoAP_Handler(RequestType type, IPAddr src_ipAddr, uint8_t *payload, uint8_t payloadSize, uint8_t *response, uint8_t *responseSize)
{
    int i;

    // We'll toggle the LED regardless of what is received to indicate any traffic
    GPIO.toggle(GPIO_6);

    if(type==CoAP_GET){
        // Return the IP address set to periodically send to
        // When filling in response data, BE CERTAIN it is AT MOST 128 bytes, or
        // the buffer will overflow!
        for(i=0;i<sizeof(DestIP);i++){
            response[i]=DestIP.byte[i];
        }
        responseSize=sizeof(DestIP);

    } else if(type == CoAP_PUT){
        // Set the IP address to periodically send to
        // First, check that size is correct
        if(payloadSize != sizeof(DestIP)){
            return;
        }

        // Copy the address
        for(i=0;i<payloadSize;i++){
            DestIP.byte[i]=payload[i];
        }

        // Enable periodic transmission
        SendPeriodicCoAPMessage=true;

    } else {
        // Unsupported request type.
        // Do nothing. 
    }

    return;
}

/**
 * @brief Periodic CoAP transmission (if destination IP is set)
 */
void SendCoAP()
{
    // Check if we are to send message. This is set to true
    // if we have received a destination IPv6 address
    if(SendPeriodicCoAPMessage != true){
        return;
    }

    // Toggle the LED to indicate that we transmit a CoAP packet
    GPIO.toggle(GPIO_7);

    // Actually send the packet
    CoAP.sendNoAck(CoAP_GET, false, CoAP_DestinationCoAPResource, CoAP_TransmissionString, sizeof(CoAP_TransmissionString));

    return;
}


/**
 * @brief This is the entry point of the user application. It is 
 *        called only once during startup. It is responsible for
 *        setting up callbacks, timers etc.
 */
RIIM_SETUP()
{
    int i;

    // Initialize variables
    SendPeriodicCoAPMessage=false;
    for(i=0;i<sizeof(DestIP);i++){
        DestIP.byte[i]=0;
    }

//    Debug.printSetup();

    // Set up GPIOs. 
    // We're using GPIO7 (Yellow LED on Radiocrafts Development Board) 
    // as indicator when we send a CoAP packet by toggling it
    // GPIO_6 (Blue LED on Radiocrafts Development Board) toggles every
    // time a CoAP packet is received on our custom CoAP resource
    GPIO.setDirection(GPIO_6, OUTPUT);
    GPIO.setDirection(GPIO_7, OUTPUT);

    // Set up custom CoAP resource
    CoAP.registerResource(CoAP_ResourceName, NULL, CoAPHandler);

    // Set network key
    const uint8_t nwKey[16]={0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
    Network.setNWKey((uint8_t*)nwKey);

    // Set channel. Only applicable for SingleChannel platforms
    Network.setChannel(32);

    // Start as a border router
    Network.startBorderRouter(NULL,NULL,NULL,NULL);
    
    // Enable and start SLIP
    Network.startSlip();

//    CoAP.connectToServer6(DestIP,false);


    // Setup timers
    timerHandler=Timer.create(PERIODIC, timerPeriod, SendCoAP);
    Timer.start(timerHandler);
    
    return UAPI_OK;
}

