MODULE_INFO_STR_LEN = 31

def is_module_info_bytes_valid(module_info_bytes):
    module_info_header = "RC188x".encode('utf-8')

    return (module_info_bytes[0:6] == module_info_header
            and len(module_info_bytes) == MODULE_INFO_STR_LEN)

def get_module_info_readable(module_info_bytes):
    """ returns human-readable version of module info string"""
    if (is_module_info_bytes_valid(module_info_bytes) == False):
        return ""

    eui = module_info_bytes[6:14]
    hardware_id = module_info_bytes[14:16]
    hardware_rev = module_info_bytes[16:18]
    platform_id = module_info_bytes[18:20]
    platform_ver = module_info_bytes[20:23]
    app_ver = module_info_bytes[23:26]
    bootloader_ver = module_info_bytes[26:29]
    bootloader_variant = module_info_bytes[29]
    lock_state = module_info_bytes[30]

    hardware_id_name = 'Unknown'
    if (hardware_id == b'\x00\x01'):
        hardware_id_name = 'RC1880'
    elif (hardware_id == b'\x00\x02'):
        hardware_id_name = 'RC1882'
    elif (hardware_id == b'\x00\x03'):
        hardware_id_name = 'RC1882HP'
    elif (hardware_id == b'\x00\x04'):
        hardware_id_name = 'RC1892HP'
    elif (hardware_id == b'\x00\x05'):
        hardware_id_name = 'RC1882HP_1_10+'
    elif (hardware_id == b'\x00\x06'):
        hardware_id_name = 'RC1880HP'
    elif (hardware_id == b'\x00\x07'):
        hardware_id_name = 'RC1890HP'

    platform_id_name = 'Unknown'
    if (platform_id == b'\x00\x01'):
        platform_id_name = 'SPR'
    elif (platform_id == b'\x00\x02'):
        platform_id_name = 'RIIM'
    elif (platform_id == b'\x00\x03'):
        platform_id_name = 'MIOTY1'

    bootloader_variant_name = 'Unknown'
    if (bootloader_variant == 0x01):
        bootloader_variant_name = 'RIIOT'
    elif (bootloader_variant == 0x02):
        bootloader_variant_name = 'RIIM'
    elif (bootloader_variant == 0x03):
        bootloader_variant_name = 'MIOTY1'

    lock_state_name = 'Unlocked'
    if (lock_state == 0x00):
        lock_state_name = 'Locked'

    s = "MODULE INFORMATION\r\n"
    s += "EUI64: " + hex_upper(eui) + "\r\n"
    s += "Hardware ID: 0x" + hex_upper(hardware_id) + ' (' + hardware_id_name + ")\r\n"
    s += "Hardware Rev: 0x" + hex_upper(hardware_rev) + "\r\n"
    s += "Platform ID: 0x" + hex_upper(platform_id) + ' (' + platform_id_name + ")\r\n"
    if(bootloader_variant != 0x02):
        s += "Platform Version: v" + get_version_str(platform_ver) + "\r\n"
    elif(bootloader_variant == 0x02):
        s += "Platform Version: v" + get_version_str_RIIM(platform_ver) + "\r\n"
    if(bootloader_variant != 0x02):
        s += "App Version: v" + get_version_str(app_ver) + "\r\n"
    s += "Bootloader Version: v" + get_version_str(bootloader_ver) + "\r\n"
    s += "Bootloader Variant: 0x" + "%.2X" % bootloader_variant + ' (' + bootloader_variant_name + ")\r\n"
    s += "Lock State: 0x" + "%.2X" % lock_state + ' (' + lock_state_name + ")\r\n"
    return s

def hex_upper(b):
    """returns hex string of bytes or byte array with upper case"""
    return b.hex().upper()

def get_version_str(b):
    """Inputs a 3-byte byte array, and converts it to version string, e.g. 1.2.3"""
    return str(b[0]) + '.' + str(b[1]) + '.' + str(b[2])

def get_version_str_RIIM(b):
    """Inputs a 3-byte byte array, and converts it to version string, e.g. 1.2.3"""
    return str(b[2]) + '.' + str(b[1]) + '.' + str(b[0])
