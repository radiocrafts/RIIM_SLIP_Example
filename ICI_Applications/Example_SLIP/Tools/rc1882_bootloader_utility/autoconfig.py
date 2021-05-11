import serial.tools.list_ports
import configparser
import time
from bl_commands import *
from module_info_string import *

def autoconfig(update_config):
    """Auto-detect serial port and write into config file
       Params:
        - update_config: boolean to indicate whether to update the config file
    """
    print ("Auto-detect serial port and update config file")

    ports_list = serial.tools.list_ports.comports()

    ftdi_list = []
    for port in ports_list:
        if (port.manufacturer == "FTDI"):
            print ("Opening ", port.device)
            try:
                ser = serial.Serial(port.device, baudrate=115200, timeout=0.01)
            except Exception as e:
                print(str(e))  ## str(e) gets just the message of exception
                continue
            # port opened successfully, add to list of port to listen
            ftdi_list.append(ser)

    if (len(ftdi_list) == 0):
        print ("No FTDI serial port found.")
        return

    print ("\r\nINSTRUCTION: Reset module into bootloader mode if it is not already")
    print ("\r\nListening......\r\n")

    port_found = test_ports(ftdi_list, 10)

    if (port_found is None):
        print ("Timed out...No Serial Port found")
    print ("Serial Port Found:", port_found)

    if (update_config):
        updateconfig(port_found)

def test_ports(port_list, duration):
    """Repeatedly test the list of ports for the module info response
       Return the port name that first responded correctly.
       Return none, if no port responded within the duration
    """

    end_time = time.time() + duration

    while (time.time() < end_time):
        for ser in port_list:
            ser.write(BL_INFO)

            module_info_bytes = ser.read(MODULE_INFO_STR_LEN)

            if (module_info_bytes is not None
                    and is_module_info_bytes_valid(module_info_bytes)):
                return ser.port

    return None
    
def updateconfig(portname):
    # updating config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    config['Default']['SerialPort'] = portname
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    print ("Config file updated")

