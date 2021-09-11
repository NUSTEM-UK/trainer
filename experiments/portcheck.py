# Reports the currently-active USB devices.
# On Mac OS, an ESP8266 will be a line like:
#     /dev/cu.usbserial-1340 - USB2.0-Serial
# On Linux, an ESP8266 will be a line like:
#     /dev/ttyUSB0 - USB2.0-Serial

import serial.tools.list_ports

ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)

