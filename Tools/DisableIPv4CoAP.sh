#!/bin/bash

sed -i 's/serverSettings.type = "udp4";/serverSettings.type = "udp6";/g' ~/.node-red/node_modules/node-red-contrib-coap/coap/coap-in.js

