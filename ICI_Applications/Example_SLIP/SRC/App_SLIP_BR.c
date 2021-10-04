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
 @brief Application to run on a border router. It sends its own address to a known 
 server (the SLIP interface). If it receives the correct response, it starts sending 
 CoAP NoAck messages to that address periodically (every 10 seconds) as well. 

 It also includes an example CoAP Handler to handle any get and set the destination
 address of the CoAP server its connected to.
*/

#include "RIIM_UAPI.h"

static const uint32_t   timerPeriod=5000;
static uint8_t timerHandle;

#define MAX_PAYLOAD_LEN 100
#define COAP_RESPONSE_OK "{\"Res\":\"Registered\"}"

// Use address 0xfd00::1:1234 as commisioning address. This is how the external network
// will get this node's IPv6 address
const IPAddr CommisioningIP={.byte={0xfd, 0x00, 0,0,0,0,0,0,0,0,0,0,0, 0x01, 0x12, 0x34}};
const uint8_t CoAP_CommisioningCoAPResource[]="CommData";

IPAddr DestIP;
bool SendPeriodicCoAPMessage=false;

const uint8_t CoAP_ResourceName[]="BRData";
const uint8_t CoAP_DestinationCoAPResource[]="ServerData";
const uint8_t CoAP_TransmissionString[]="Hello, World!";

void CoAPHandler(RequestType type, IPAddr src_ipAddr, uint8_t *payload, uint8_t payloadSize, uint8_t *response, uint8_t *responseSize)
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
        *responseSize=sizeof(DestIP);

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

        // Connect to server
        CoAP.disconnectFromServer();
        CoAP.connectToServer6(DestIP,false);

    } else {
        // Unsupported request type.
        // Do nothing. 
    }

    return;
}

/**
 * @brief Send temperature as a JSON string
 */
void SendTemperature()
{
    uint8_t MsgSize;

    // Toggle the LED to indicate that we transmit a CoAP packet
    GPIO.toggle(GPIO_7);

    char TemperatureJSONString[MAX_PAYLOAD_LEN];
    MsgSize=Util.snprintf(TemperatureJSONString, MAX_PAYLOAD_LEN, "{\"Temp\":\"%d\"}", Util.getTemperature());
    CoAP.sendNoAck(CoAP_PUT,false,"ServerData",TemperatureJSONString,MsgSize);
}

/**
 * @brief Send commisioning packet. This is our own IPv6 address.
 */
void SendCommisioning()
{
    int i;
    IPAddr MyIPAddr;


    // Toggle the LED to indicate that we transmit a CoAP packet
    GPIO.toggle(GPIO_7);

    // Check if we are to send a regular message. 
    // This is set to true if we have received a destination IPv6 address
    // If not: Send message to commisioning IP address insteead consisting of
    // our own address
    if(SendPeriodicCoAPMessage != true){
        Network.getAddress(&MyIPAddr);
        CoAP.send(CoAP_PUT, false, CoAP_CommisioningCoAPResource, (uint8_t*)&MyIPAddr, sizeof(MyIPAddr));
        return;
    }

    // Actually send the packet
    CoAP.sendNoAck(CoAP_GET, false, CoAP_DestinationCoAPResource, CoAP_TransmissionString, sizeof(CoAP_TransmissionString));

    return;
}

/**
 * @brief Check for responses
 */
void CoAP_ResponseHandler(const uint8_t *payload, uint8_t payload_size)
{
    if(Util.strcmp(payload, COAP_RESPONSE_OK)==0){
        GPIO.setValue(GPIO_6, HIGH); // Indicate node is commisioned
        Timer.stop(timerHandle);
        timerHandle=Timer.create(PERIODIC, timerPeriod, SendTemperature);
        Timer.start(timerHandle);
    }

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
    GPIO.setValue(GPIO_6, LOW);
    GPIO.setValue(GPIO_7, LOW);

    // Set up custom CoAP resource
    CoAP.registerResource(CoAP_ResourceName, NULL, CoAPHandler);
    CoAP.registerResponseHandler(CoAP_ResponseHandler);

    // Set network key
    const uint8_t nwKey[16]={10,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
    Network.setNWKey((uint8_t*)nwKey);

    Network.setPanId(0x1134);
    Network.setChannel(32);
    Network.setFreqBand(RF_BAND_868);
    Network.setTxPower(14);
    Network.setTschMaxBroadcastRate(8); // To speed up joining time in TSCH
//    Network.setTSCHParameters(TSCH_HIGH_THROUGHPUT_SENSOR_DATA);

    // Set channel. Only applicable for SingleChannel platforms
    Network.setChannel(32);

    // Start as a border router
//    Network.startBorderRouter(NULL,NULL,NULL,NULL);
    
    // Enable and start SLIP
    Network.startSlip();

    // Register commisioning address
    CoAP.connectToServer6(CommisioningIP,false);

    // Setup timers
    timerHandle=Timer.create(PERIODIC, timerPeriod, SendCommisioning);
    Timer.start(timerHandle);
    
    return UAPI_OK;
}

