#!/usr/bin/env python3

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

import sys
import configparser
import argparse
import serial
import re
import time
import binascii
from defs import *
from module_info_string import *
from load_image import load_image
from load_key import load_key



def is_cmd_valid(cmd):
    """ 
    Check if command exists 
    """
    if cmd in command_list:
        return True
    return False

def error_exit(msg):
    """ 
    Print error and exit the application
    """
    print ("Error: " + msg)
    sys.exit(1)

def print_BL_error(error_str):
    """
    Prints the error status from bootloader
    """
    if error_str in error_table:
        print ("Bootloader Error: " + error_table[error_str])
    else:
        print ("Unknown Bootloader Error: " + error_str)


def MAIN(args):
    """ 
    Main function
    """

    # Extract arguments and set default values
    command = args.command
    cmd_arg=args.arg
    test_open_file = None

    # Check if command is valid
    if (is_cmd_valid(command) == False):
        error_exit('\"' + command + '\"' + " is an unrecognized command")

    # If file argument is specified, then load and validate the file exists
    if args.file is not None:
        try:
            test_open_file = open(args.file, 'rb')
            test_open_file.close()
        except Exception as e:
            error_exit(str(e))

    # Retries is done every 50ms
    connection_timeout = int(args.timeout)*20


    # If serial port is specified in command line, use that
    # Otherwise, use the default in the configuration file
    if args.port is not None:
        serial_port_name = args.port
    else:
        # Read the configuration file and get the serial port
        config = configparser.ConfigParser()
        config.read('config.ini')
        serial_port_name = config['Default']['SerialPort']

    # Open serial port
    try:
        ser = serial.Serial(serial_port_name, baudrate=115200, timeout=0.05)
    except Exception as e:
        error_exit(str(e))  ## str(e) gets just the message of exception
    # Check if serial port is connected to a RC188x bootloader in serial mode.
    # Does so by sending INFO command, and then check if bootloader responds with
    # Module Information String
    for i in range (connection_timeout):
       ser.write(BL_INFO)
       module_info_bytes = ser.read(MODULE_INFO_STR_LEN)
       if (is_module_info_bytes_valid(module_info_bytes) == False):
           if(i % 20 == 0):
              print("Cannot connect to Bootloader (Press RESET on board?). Attempt ", (i/20)+1 ," of ", connection_timeout/20, ".")
           if(i+1 == connection_timeout):
               error_exit("Failed to connect to bootloader.")
               # Delay is given by timeout when setting up "ser"
       else:
           break

    ser.timeout=1 # Set serial timeout to 1 second

    print (get_module_info_readable(module_info_bytes))

    wait_for_bl_result = True

    if command in command_list:
        command_list[command](args, ser)


    # Wait for bootloader to output success/error result
    if wait_for_bl_result == True:
        # While not timed out, and not having received both result and module info string
        # Read 1 byte at time, add to saved buffer.
        # After reading each byte, apply regular expression to saved buffer
        # to check if a success or error result was outputted. 
        # If so, interpret and print out a user-friendly string
        print ("Waiting for bootloader status..")
        ser.timeout = 10
        received_result = False
        rx_buffer = bytearray()
        while (received_result == False):
            read_byte = ser.read(1)
            # if nothing read then timeout
            if len(read_byte) == 0:
                break;

            rx_buffer += read_byte

            # check for OK result
            match = re.search(b'OKOK', rx_buffer)
            if match is not None:
                print ("Bootloader Status: Success")
                received_result = True
                break;

            # check for ERR result, ERR followed by a number digi
            match = re.search(b'ERR\d', rx_buffer)
            if match is not None:
                print_BL_error(match.group(0).decode('utf-8'))
                received_result = True
                break;

        if received_result is False:
            print ("Error: Timed out waiting for result status from Bootloader");


def CMD_Info_Func(args, ser):
    """ 
    Function for returning module info.
    """
    # Already got the module info on startup. Application can exit
    sys.exit()

def CMD_Load_Image_Func(args, ser):
    """ 
    Function for loading image onto module
    """
    print ("Loading Image")
    if args.file is None:
        error_exit("No image file specified")
    upload_result = load_image(ser, args.file)

    if (upload_result == False):
        error_exit("Image transfer failed.")


def CMD_Lock_Func(args, ser):
    """ 
    Function for locking module
    """
    print ("Locking Module")
    ser.write(BL_LOCK)


def CMD_Load_App_Image_Key_Func(args, ser):
    """ 
    Function for loading ICI application key
    """
    print ("Loading App Image Key")
    if args.file is None:
        error_exit("No key file specified")
    result = load_key(BL_AKEY, key_size_table[BL_AKEY], args.file, ser)

    if (result == False):
        error_exit("Loading key failed.")


def CMD_Load_Network_Key_Func(args, ser):
    """ 
    Function for loading default network key
    """
    print ("Loading Network Key")
    if args.file is None:
        error_exit("No key file specified")
    result = load_key(BL_NKEY, key_size_table[BL_NKEY], args.file, ser)

    if (result == False):
        error_exit("Loading key failed.")
            

def CMD_Run_App_Func(args, ser):
    """ 
    Function for exiting BSL and start ICI application and platform
    """
    print ("Exit the Bootloader to start running the Application")
    ser.write(BL_EXIT)


# Commands
command_list={
    'info'                : CMD_Info_Func,
    'load-image'          : CMD_Load_Image_Func,
    'lock'                : CMD_Lock_Func,
    'load-app-image-key'  : CMD_Load_App_Image_Key_Func,
    'load-network-key'    : CMD_Load_Network_Key_Func,
    'run-app'             : CMD_Run_App_Func
}

# Entry point
if __name__ == "__main__":

    # RC Extensions are for internal Radiocrafts use only
    try:
        from RC_Internal.RC_Extensions import RCExtensions_Init
        RCExtensions_Init(command_list)
    except:
        # Contiunue execution
        pass

    # Setup argparser
    parser = argparse.ArgumentParser(prog=APP_NAME)
    parser.add_argument('--version', action='version', version='%(prog)s v' + VERSION)
    parser.add_argument("command", help="info, load-image, load-app-image-key, load-network-key, lock, run-app")
    parser.add_argument('-f', "--file", help="image or key file")
    parser.add_argument('-a', "--arg", help="Argument")
    parser.add_argument('-p', "--port", help="Serial port, e.g. COM12. If unspecified, then the default in the config file is used")
    parser.add_argument('-t', "--timeout", help="Timeout (in seconds) for trying to connect to bootloader. Default is 10 seconds" , default=10)
    # load arguments
    args = parser.parse_args()

    MAIN(args)