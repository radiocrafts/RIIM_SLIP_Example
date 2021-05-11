import bootloader_util as bu

def test_is_module_info_str_valid():
    bad_header = "RC192xABCDEABCDEABCDEABCDEABCD".encode('utf-8')
    bad_len = "RC188x0123456".encode('utf-8')
    correct = "RC188x012345678901234567890123".encode('utf-8')
    assert bu.is_module_info_bytes_valid(bad_header) == False
    assert bu.is_module_info_bytes_valid(bad_len) == False
    assert bu.is_module_info_bytes_valid(correct) == True

def test_display_module_info():
    info_header = "RC188x".encode('utf-8')
    eui_hex = "0A0B0C0D0E0F0102"
    hardware_id_hex = "0001"
    hardware_rev_hex = "A001"
    platform_id_hex = "0001"
    platform_ver_hex = "111213"
    app_ver_hex = "141516"
    bootloader_ver_hex = "171819"
    lock_state_hex = "FF"

    info_hex = (eui_hex + hardware_id_hex + hardware_rev_hex 
               + platform_id_hex + platform_ver_hex + app_ver_hex
               + bootloader_ver_hex + lock_state_hex)
    info_bytes = bytearray(info_header)
    info_bytes += bytes.fromhex(info_hex)

    ## expected string
    es = "MODULE INFORMATION\r\n"
    es += "EUI64: 0A0B0C0D0E0F0102\r\n"
    es += "Hardware ID: 0x0001 (RC1880)\r\n"
    es += "Hardware Rev: 0xA001\r\n"
    es += "Platform ID: 0x0001 (SPR)\r\n"
    es += "Platform Version: v17.18.19\r\n"
    es += "App Version: v20.21.22\r\n"
    es += "Bootloader Version: v23.24.25\r\n"
    es += "Lock State: 0xFF (Unlocked)\r\n"

    ## no assert, just checking module info
    print (bu.get_module_info_readable(info_bytes))
    assert es == bu.get_module_info_readable(info_bytes)

def test_display_module_info_2():
    info_header = "RC188x".encode('utf-8')
    eui_hex = "0A0B0C0D0E0F0102"
    hardware_id_hex = "035A"
    hardware_rev_hex = "A001"
    platform_id_hex = "0103"
    platform_ver_hex = "111213"
    app_ver_hex = "141516"
    bootloader_ver_hex = "171819"
    lock_state_hex = "00"

    info_hex = (eui_hex + hardware_id_hex + hardware_rev_hex 
               + platform_id_hex + platform_ver_hex + app_ver_hex
               + bootloader_ver_hex + lock_state_hex)
    info_bytes = bytearray(info_header)
    info_bytes += bytes.fromhex(info_hex)

    ## expected string
    es = "MODULE INFORMATION\r\n"
    es += "EUI64: 0A0B0C0D0E0F0102\r\n"
    es += "Hardware ID: 0x035A (Unknown)\r\n"
    es += "Hardware Rev: 0xA001\r\n"
    es += "Platform ID: 0x0103 (Unknown)\r\n"
    es += "Platform Version: v17.18.19\r\n"
    es += "App Version: v20.21.22\r\n"
    es += "Bootloader Version: v23.24.25\r\n"
    es += "Lock State: 0x00 (Locked)\r\n"

    ## no assert, just checking module info
    print (bu.get_module_info_readable(info_bytes))
    assert es == bu.get_module_info_readable(info_bytes)
