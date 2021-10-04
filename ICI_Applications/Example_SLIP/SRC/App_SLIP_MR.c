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
 @brief Application to run on a mesh router. It sends its own address to a known 
 server (the SLIP interface). If it receives the correct response, it starts sending 
 CoAP NoAck messages to that address periodically (every 10 seconds) as well. 
*/

#include "RIIM_UAPI.h"

#define MAX_PAYLOAD_LEN 100
#define COAP_RESPONSE_OK "{\"Res\":\"Registered\"}"

static const uint32_t   timerPeriod=10000;
static uint8_t timerHandle;
const IPAddr CommisioningIP={.byte={0xfd, 0x00, 0,0,0,0,0,0,0,0,0,0,0, 0x01, 0x12, 0x34}};

const uint8_t CoAP_CommisioningCoAPResource[]="CommData";

IPAddr DestIP;
bool SendPeriodicCoAPMessage=false;

const uint8_t CoAP_ResourceName[]="BRData";
const uint8_t CoAP_DestinationCoAPResource[]="ServerData";


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

    Util.printf("Trying to commision...");
    if(Network.getNetworkState()==ONLINE){

        // Toggle the LED to indicate that we transmit a CoAP packet
        GPIO.toggle(GPIO_7);

        if(SendPeriodicCoAPMessage != true){
            Network.getAddress(&MyIPAddr);
            CoAP.send(CoAP_PUT, false, CoAP_CommisioningCoAPResource, (uint8_t*)&MyIPAddr, sizeof(MyIPAddr));
            Util.printf("Packet sent!\n");
            return;
        }
    } else {
        Util.printf("\n");
    }

    return;
}

/**
 * @brief Check for responses
 */
void CoAP_ResponseHandler(const uint8_t *payload, uint8_t payload_size)
{
    char responseStr[MAX_PAYLOAD_LEN];

    Util.printf("Got response:\n");
    Util.snprintf(responseStr, MAX_PAYLOAD_LEN, "%s",payload);
    Util.printf(responseStr);
    Util.printf("\n");
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
    // Initialize UART
//    UART.init(115200, UART_PARITY_NONE, UART_DATA_8_BITS, UART_STOP_1_BIT);

    Debug.printSetup();

    // Start as a router, leaf or border router.
    const uint8_t nwKey[16]={10,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
    Network.setNWKey((uint8_t*)nwKey);
    Network.setPanId(0x1134);
    Network.setChannel(32);
    Network.setFreqBand(RF_BAND_868);
    Network.setTxPower(14);
    Network.setTschMaxBroadcastRate(8); // To speed up joining time in TSCH

    Network.startMeshRouter();
    Network.setChannel(32);

    GPIO.setDirection(GPIO_7, OUTPUT);
    GPIO.setValue(GPIO_7, HIGH);

    CoAP.registerResponseHandler(CoAP_ResponseHandler);

    // Register commisioning address
    CoAP.connectToServer6(CommisioningIP,false);

    // Setup timers
    timerHandle=Timer.create(PERIODIC, timerPeriod, SendCommisioning);
    Timer.start(timerHandle);
    
    return UAPI_OK;
}

