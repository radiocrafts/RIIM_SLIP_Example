#*****************************************************************************
#* Copyright ©2021. Radiocrafts AS (Radiocrafts).  All Rights Reserved. 
#* Permission to use, copy, modify, and distribute this software and 
#* its documentation, without fee and without a signed licensing 
#* agreement, is hereby granted, provided that the above copyright 
#* notice, this paragraph and the following two paragraphs appear in 
#* all copies, modifications, and distributions.
#* 
#* IN NO EVENT SHALL RADIOCRFTS BE LIABLE TO ANY PARTY FOR DIRECT, 
#* INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING 
#* LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS 
#* DOCUMENTATION, EVEN IF RADIOCRAFTS HAS BEEN ADVISED OF THE 
#* POSSIBILITY OF SUCH DAMAGE. 
#* 
#* RADIOCRAFTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT 
#* NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND 
#* FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE AND ACCOMPANYING 
#* DOCUMENTATION, IF ANY, PROVIDED HEREUNDER IS PROVIDED "AS IS". 
#* RADIOCRAFTS HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, 
#* UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
#****************************************************************************/

# Uses XMODEM to transfer an image
from defs import *
import xmodem

def load_image(ser, image_file_path):
    """
    Loads an image to BSL using XMODEM
    Args:
        ser: serialport object, already opened
        image_file_path: path to image file, already verified
    Returns true if file upload successful; otherwise false

    Sends BSL command 'IMAG' to activate XMODEM mode.
    wait for BSL to send NAK before initiating transfer.
    when XMODEM transfer complete, display progress report from BSL
    on validation, and loading. When BSL reports it has either 
    loaded the image to internal flash, or rejected image as invalid, 
    then return and exit
    """
    print ("Waiting for BSL to initiate transfer...")
    ser.write(BL_IMAG)

    image_file = open(image_file_path, 'rb')
    result = xmodem.send(ser, image_file)
    if result == True:
        print ("file upload successful")
    else:
        print ("file upload failed")

    image_file.close()

    return result

            
