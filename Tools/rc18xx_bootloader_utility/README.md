# Bootloader Utility
The bootloader utility can be used to communicate with the persistent bootloader located on the RC18xx modules

## Commands
Commands for reading info, locking, setting keys and loading application and platform are provided.

### info
Prints module info

Example:
rc188x_bootloader_utility.py info -p /dev/ttyUSB0

### load-image
Loads image (ICI application or Platform) onto module

Example:
rc188x_bootloader_utility.py load-image -p /dev/ttyUSB0 -f Filename.bin

### lock
Lock the module. After locking, no changes to keys are allowed. 
Changes to software is only allowed for encrypted images

Example:
rc188x_bootloader_utility.py lock -p /dev/ttyUSB0

### load-app-image-key
Load image encryption key. ICI applications must be encrypted with the same key.

Example:
rc188x_bootloader_utility.py load-app-image-key -p /dev/ttyUSB0 -f Keyfile.key

### load-network-key
Load default network key. This can be overridden in the ICI application

Example:
rc188x_bootloader_utility.py load-network-key info -p /dev/ttyUSB0 -f Keyfile.key

### run-app
Exit BSL mode and start Platform and ICI application

Example:
rc188x_bootloader_utility.py run-app -p /dev/ttyUSB0
