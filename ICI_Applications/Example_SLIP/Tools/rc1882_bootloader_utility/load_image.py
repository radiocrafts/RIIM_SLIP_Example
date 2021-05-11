# Uses XMODEM to transfer an image
import xmodem
from bl_commands import *

def load_image(ser, image_file_path):
    """
    Loads an image to bootloader using XMODEM
    Args:
        ser: serialport object, already opened
        image_file_path: path to image file, already verified
    Returns true if file upload successful; otherwise false

    Sends bootloader command 'IMAG' to activate XMODEM mode.
    wait for bootloader to send NAK before initiating transfer.
    when XMODEM transfer complete, display progress report from bootloader
    on validation, and loading. When bootloader reports it has either 
    loaded the image to internal flash, or rejected image as invalid, 
    then return and exit
    """
    print ("Waiting for Bootloader to initiate transfer...")
    ser.write(BL_IMAG)

    image_file = open(image_file_path, 'rb')
    result = xmodem.send(ser, image_file)
    if result == True:
        print ("file upload successful")
    else:
        print ("file upload failed")

    image_file.close()

    return result

            
