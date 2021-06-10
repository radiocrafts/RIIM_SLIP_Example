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

from defs import *

MODULE_INFO_STR_LEN = 31

def is_module_info_bytes_valid(module_info_bytes):
    """
    Check if info bytes are valid
    """
    module_info_header = "RC188x".encode('utf-8')

    return (module_info_bytes[0:6] == module_info_header
            and len(module_info_bytes) == MODULE_INFO_STR_LEN)

def get_module_info_readable(module_info_bytes):
    """ 
    Returns human-readable version of module info string
    """
    if (is_module_info_bytes_valid(module_info_bytes) == False):
        return ""

    eui = module_info_bytes[6:14]
    hardware_id = module_info_bytes[14:16]
    hardware_rev = module_info_bytes[16:18]
    platform_id = module_info_bytes[18:20]
    platform_ver = module_info_bytes[20:23]
    app_ver = module_info_bytes[23:26]
    bootloader_ver = module_info_bytes[26:29]
    bootloader_variant_id = module_info_bytes[29]
    lock_state_id = module_info_bytes[30]

    if hardware_id in hardware_id_name_table:
        hardware_id_name = hardware_id_name_table[hardware_id]
    else:
        hardware_id_name = 'Unknown'

    if platform_id in platform_id_name_table:
        platform_id_name = platform_id_name_table[platform_id]
    else:
        platform_id_name = 'Unknown'

    if bootloader_variant_id in bootloader_variant_id_name_table:
        bootloader_variant_id_name = bootloader_variant_id_name_table[bootloader_variant_id]
    else:
        bootloader_variant_id_name = 'Unknown'

    if lock_state_id in lock_state_id_name_table:
        lock_state_id_name = lock_state_id_name_table[lock_state_id]
    else:
        lock_state_id_name = 'Unknown'


    s = "MODULE INFORMATION\r\n"
    s += "EUI64: " + hex_upper(eui) + "\r\n"
    s += "Hardware ID: 0x" + hex_upper(hardware_id) + ' (' + hardware_id_name + ")\r\n"
    s += "Hardware Rev: 0x" + hex_upper(hardware_rev) + "\r\n"
    s += "Platform ID: 0x" + hex_upper(platform_id) + ' (' + platform_id_name + ")\r\n"
    s += "Platform Version: v" + get_version_str(platform_ver) + "\r\n"
    s += "App Version: v" + get_version_str(app_ver) + "\r\n"
    s += "Bootloader Version: v" + get_version_str(bootloader_ver) + "\r\n"
    s += "Bootloader Variant: 0x" + "%.2X" % bootloader_variant_id + ' (' + bootloader_variant_id_name + ")\r\n"
    s += "Lock State: 0x" + "%.2X" % lock_state_id + ' (' + lock_state_id_name + ")\r\n"
    return s

def hex_upper(b):
    """
    Returns hex string of bytes or byte array with upper case
    """
    return b.hex().upper()

def get_version_str(b):
    """
    Inputs a 3-byte byte array, and converts it to version string, e.g. 1.2.3
    """
    return str(b[2]) + '.' + str(b[1]) + '.' + str(b[0])
