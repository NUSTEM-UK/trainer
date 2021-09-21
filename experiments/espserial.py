# Very basic serial port experiment
# After https://techtutorialsx.com/2017/12/02/esp32-esp8266-arduino-serial-communication-with-python/

import serial

ser = serial.Serial()
ser.baudrate = 115200
# Need to autodetect serial port - see portcheck.py
ser.port = "/dev/cu.usbserial-1340"
ser.open()

# This is in the original article, but barfs for me in Python3
# values = bytearray([4, 9, 62, 144, 56, 30, 147, 3, 210, 89, 111, 78, 184, 151, 17, 129])
# ser.write(values)

#...whereas this works as we'd expect. Note the encode and decode steps.
# - Unicode strings are not handle
myString = "Hello world!"
ser.write(myString.encode())

total = 0

while total < len(myString):
    received = str(ser.read(1).decode("utf-8"))
    # print(ser.read(1))
    print(received)
    total += 1

ser.close();
