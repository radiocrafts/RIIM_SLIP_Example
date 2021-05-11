from bl_commands import *
import serial

# maps BL command to key size
key_size_table = {
    BL_AKEY: 16,
    BL_NKEY: 16,
    BL_LICN: 24,
}

def load_key(bl_cmd, key_file_path, ser):
    """
    Loads a key to bootloader. 
    Could be app image key, network key, or license key
    Args:
        bl_cmd: either BL_AKEY, or BL_NKEY, BL_LICN 
        key_file_path: path to key file, already verified to exist
        ser: serial port
    """

    # open file to read it as a string
    key_file = open(key_file_path, 'r')

    key_size = key_size_table[bl_cmd]
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
