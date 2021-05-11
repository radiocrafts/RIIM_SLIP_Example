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
 @brief Application to run on a mesh router. The application sets up a custom
 CoAP resource called "data" that responds to incoming requests. Also, if it 
 receives a PUT with an IPv6 address, it starts sending CoAP NoAck messages to that
 address periodically (every 10 seconds) as well. To aid debugging, it prints out
 the source and destination address on UART as well
 @version 1.0.0
 @date 2021.04.23
*/

#include "RIIM_UAPI.h"

static const uint32_t   timerPeriod=10000;
static uint8_t timerHandler;
const IPAddr DestIP={.byte={0x20, 0x01, 0x46, 0x46, 0xf8, 0x86,0,0,0,0,0,0,0 ,0x01,0x12,0x34}};

/**
 * @brief Callback for UART TX/transmission
 */
void SendCoAP()
{
    IPAddr addr;
    if(Network.getNetworkState()==ONLINE){
        GPIO.toggle(GPIO_7);
        CoAP.sendNoAck(CoAP_GET,false,"tst","test",5);
        Network.getAddress(&addr);
        Debug.printIPAddr(&addr);
        Util.printf(" -> ");
        Debug.printIPAddr(&DestIP);
        Util.printf("\n");
    } else {
        Util.printf(".");
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

//    Debug.printSetup();

    // Start as a router, leaf or border router.
    const uint8_t nwKey[16]={0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
    Network.setNWKey((uint8_t*)nwKey);
    Network.startMeshRouter();
    Network.setChannel(32);

    GPIO.setDirection(GPIO_7, OUTPUT);
    CoAP.connectToServer6(DestIP,false);

    // Setup timers
    timerHandler=Timer.create(PERIODIC, timerPeriod, SendCoAP);
    Timer.start(timerHandler);
    
    return UAPI_OK;
}

