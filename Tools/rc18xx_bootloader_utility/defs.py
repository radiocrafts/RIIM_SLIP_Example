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

APP_NAME = "bootloader_util"
VERSION = "1.7.0"

hardware_id_name_table = {
    b'\x00\x01' : 'RC1880',
    b'\x00\x02' : 'RC1882',
    b'\x00\x03' : 'RC1882HP', 
    b'\x00\x04' : 'RC1892HP',
    b'\x00\x05' : 'RC1882HP_1_10+',
    b'\x00\x06' : 'RC1880HP',
    b'\x00\x07' : 'RC1890HP'
}

platform_id_name_table = {
    b'\x00\x01' : 'SPR',
    b'\x00\x02' : 'RIIM',
    b'\x00\x03' : 'MIOTY1'
}

bootloader_variant_id_name_table = {
    0x00 : 'RIIOT',
    0x01 : 'RIIM',
    0x02 : 'MIOTY1'
}

lock_state_id_name_table = {
    0x00 : 'Locked',
    0xFF : 'Unlocked'
}

# Error string and description table
error_table = {
    'ERR1': 'Bad image length',
    'ERR2': 'Bad image CRC',
    'ERR3': 'Bad image hardware info',
    'ERR4': 'Bad image authentication',
    'ERR5': 'Error writing flash',
    'ERR6': 'Module is locked'
}

## Bootloader command names, encoded in bytes that can be sent over serial port
## all end with return character
BL_INFO = b'INFO\r'
BL_IMAG = b'IMAG\r'
BL_LOCK = b'LOCK\r'
BL_NKEY = b'NKEY\r'
BL_AKEY = b'AKEY\r'
BL_EXIT = b'EXIT\r'

# maps BL command to key size
key_size_table = {
    BL_AKEY: 16,
    BL_NKEY: 16
}

