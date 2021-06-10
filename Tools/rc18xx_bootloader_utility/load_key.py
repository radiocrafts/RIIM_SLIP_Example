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

import serial
from defs import *


def load_key(bl_cmd, key_size, key_file_path, ser):
    """
    Loads a key to bootloader. 
    Args:
        bl_cmd: either BL_AKEY, BL_NKEY
        key_file_path: path to key file
        ser: serial port
    """

    # open file to read it as a string
    key_file = open(key_file_path, 'r')

    key_hex_str_size = key_size * 2

    # verify key file contains a hex string with length that matches expected key length
    file_content = key_file.read()

    if len(file_content) < key_hex_str_size:
        key_file.close()
        print ("Key file must contain a hex string of %d characters (%d bytes)", 
                key_hex_str_size, key_size)
        return False

    # get the first exact number of bytes needed for the key hex string
    # discard the rest
    key_hex_str = file_content[:key_hex_str_size]

    try:
        key_bytes = bytes.fromhex(key_hex_str)
    except Exception as e: 
        key_file.close()
        print ("Key contains non-hex values")
        return False

    # write the bootloader serial command, followed by the key bytes
    ser.write(bl_cmd)
    ser.write(key_bytes)

    key_file.close()

    return True
