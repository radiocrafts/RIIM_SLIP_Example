#!/usr/bin/env python3

import sys
import configparser
import argparse
import serial
import re
import time
import binascii
from module_info_string import *
from load_image import load_image
from load_key import load_key
from bl_commands import *
#from autoconfig import autoconfig

APP_NAME = "bootloader_util"
VERSION = "1.6.0"

# list of CLI commands
CMD_INFO = 'info'
CMD_LOAD_IMAGE = 'load-image'
CMD_LOCK = 'lock'
CMD_LOAD_APP_IMAGE_KEY = 'load-app-image-key'
CMD_LOAD_NETWORK_KEY = 'load-network-key'
CMD_LOAD_LICENSE_KEY = 'load-license-key'
CMD_RUN_APP = 'run-app'
CMD_CW_TEST = 'cw-test'
CMD_MOD_TEST = 'modulated-test'
CMD_RX_TEST = 'rx-test'
CMD_RADIO_OFF = 'radio-off'
CMD_SPI_TEST = 'spi-test'
CMD_I2C_TEST = 'i2c-test'
CMD_SLEEP_TEST = 'sleep-test'
CMD_READ_CALIBRATION = 'read-calibration'
CMD_WRITE_CALIBRATION = 'write-calibration'
CMD_READ_SERIAL = 'read-serial'
CMD_WRITE_SERIAL = 'write-serial'
CMD_WRITE_TEMP_CAPARRAY = 'write-temp-caparray'

cmd_list = [CMD_INFO, CMD_LOAD_IMAGE, CMD_LOCK, CMD_LOAD_APP_IMAGE_KEY, 
            CMD_LOAD_NETWORK_KEY, CMD_LOAD_LICENSE_KEY, CMD_RUN_APP, 
            CMD_CW_TEST, CMD_MOD_TEST, CMD_RX_TEST, CMD_RADIO_OFF,
            CMD_SPI_TEST, CMD_I2C_TEST, CMD_SLEEP_TEST, 
            CMD_READ_CALIBRATION, CMD_WRITE_CALIBRATION, 
            CMD_READ_SERIAL, CMD_WRITE_SERIAL, CMD_WRITE_TEMP_CAPARRAY
            ]

# Error string and description table
error_table = {
    'ERR1': 'Bad image length',
    'ERR2': 'Bad image CRC',
    'ERR3': 'Bad image hardware info',
    'ERR4': 'Bad image authentication',
    'ERR5': 'Error writing flash',
    'ERR6': 'Module is locked',
    'ERR7': 'Cannot re-write license',
    'ERR8': 'Error erasing flash',
    'ERR9': 'Error accessing SPI flash'
}

def is_cmd_valid(cmd):
    for c in cmd_list:
        if c == cmd:
            return True
    return False

def error_exit(msg):
    print ("Error: " + msg)
    sys.exit()

def print_BL_error(error_str):
    """Prints the error status from bootloader
    Args:
        error_str: error string printed by bootloader
    """
    if error_str in error_table:
        print ("Bootloader Error: " + error_table[error_str])
    else:
        print ("Unknown Bootloader Error: " + error_str)

'''
Main Execution
'''
def MAIN(args):

    command = args.command
    cmd_arg=args.arg
    test_open_file = None

    if (is_cmd_valid(command) == False):
        error_exit('\"' + command + '\"' + " is an unrecognized command")

    # if file argument is specified, then load and validate the file exists
    if args.file is not None:
        try:
            test_open_file = open(args.file, 'rb')
            test_open_file.close()
        except Exception as e:
            error_exit(str(e))

    # for the commands that require a file, check the file exists
    if (command == CMD_LOAD_IMAGE
        and test_open_file is None):
        error_exit("No image file specified")

    # Retries is done every 50ms
    connection_timeout = int(args.timeout)*20


    # if serial port is specified in command line, use that
    # Otherwise, use the default in the configuration file
    if args.port is not None:
        serial_port_name = args.port
    else:
        # read the configuration file and get the serial port
        config = configparser.ConfigParser()
        config.read('config.ini')
        serial_port_name = config['Default']['SerialPort']

    if ((command == CMD_LOAD_APP_IMAGE_KEY
         or command == CMD_LOAD_NETWORK_KEY
         or command == CMD_LOAD_LICENSE_KEY)
        and test_open_file is None):
        error_exit("No key file specified")

    # open serial port
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
              print("Cannot connect to Bootloader. Failed attempt ", (i/20)+1 ," of ", connection_timeout/20, ".")
           if(i+1 == connection_timeout):
               error_exit("Failed to connect to bootloader.")
               # Delay is given by timeout when setting up "ser"
       else:
           break

    ser.timeout=1 # Set serial timeout to 1 second

    print (get_module_info_readable(module_info_bytes))

    ''' 
    Take different actions depending on the command.
    load image
    load key
    '''
    wait_for_bl_result = True
    if command == CMD_INFO:
        # already got the module info. can exit
        sys.exit()

    elif command == CMD_LOAD_IMAGE:
        print ("Loading Image")
        upload_result = load_image(ser, args.file)

        if (upload_result == False):
            error_exit("Image transfer failed.")

    elif command == CMD_LOCK:
        print ("Locking Module")
        ser.write(BL_LOCK)

    elif command == CMD_LOAD_APP_IMAGE_KEY:
        print ("Loading App Image Key")
        result = load_key(BL_AKEY, args.file, ser)

        if (result == False):
            error_exit("Loading key failed.")

    elif command == CMD_LOAD_NETWORK_KEY:
        print ("Loading Network Key")
        result = load_key(BL_NKEY, args.file, ser)

        if (result == False):
            error_exit("Loading key failed.")
            
    elif command == CMD_LOAD_LICENSE_KEY:
        print ("Loading License Key")
        result = load_key(BL_LICN, args.file, ser)

        if (result == False):
            error_exit("Loading key failed.")

    elif command == CMD_RUN_APP:
        print ("Exit the Bootloader to start running the Application")
        ser.write(BL_EXIT)

    elif command == CMD_CW_TEST:
        print ("Starting CW test")
        time.sleep(0.1)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(BL_CWTS)

    elif command == CMD_MOD_TEST:
        print ("Starting modulated output test")
        time.sleep(0.1)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(BL_MTST)

    elif command == CMD_RX_TEST:
        print("Starting RX test")
        time.sleep(0.1)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(BL_RXEN)

    elif command == CMD_RADIO_OFF:
        print("Turning off radio")
        time.sleep(0.1)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(BL_ROFF)

    elif command == CMD_SPI_TEST:
        print("Testing SPI")
        time.sleep(0.1)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(BL_SPIF)

    elif command == CMD_I2C_TEST:
        print("Testing I2C")
        time.sleep(0.1)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(BL_I2CE)

    elif command ==CMD_SLEEP_TEST:
        print("Entering sleep. NB: Module must be reset to exit sleep mode")
        time.sleep(0.1)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(BL_SLEE)

    elif command == CMD_READ_CALIBRATION:
        time.sleep(0.1)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        sendstr=b'' + BL_RCAL + binascii.unhexlify(cmd_arg) + b"  " # Append two dummybytes
        ser.write(sendstr)
        print ("Reading calibration "+ cmd_arg + ": " + binascii.hexlify(ser.read(2)).decode("ascii"))
    
    elif command == CMD_WRITE_CALIBRATION:
        print ("Writing calibration: " + cmd_arg)
        sendstr=b'' + BL_WCAL + binascii.unhexlify(cmd_arg)
        ser.write(sendstr)

    elif command == CMD_READ_SERIAL:
        time.sleep(0.1)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        ser.write(BL_RSER)
        print("Read serial number : " + binascii.hexlify(ser.read(8)).decode("ascii"))

    elif command == CMD_WRITE_SERIAL:
        print("Writing serial number : " + cmd_arg)
        time.sleep(0.1)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        sendstr=b'' + BL_WSER + binascii.unhexlify(cmd_arg)
        ser.write(sendstr)

    elif command == CMD_WRITE_TEMP_CAPARRAY:
        print("Writing cap array : " + cmd_arg)
        time.sleep(0.1)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        sendstr=b'' + BL_CAPA + binascii.unhexlify(cmd_arg)
        ser.write(sendstr)

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

if __name__ == "__main__":
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