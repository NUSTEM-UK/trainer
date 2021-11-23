# UART1 on pins GP4/5 RX/TX

from machine import UART, Pin
import utime

# self.uart = UART(uartNum, 9600, parity=None, stop=1, bits=8, rx=rxPin, tx=txPin)
uart1 = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

while True:
    print('Awaiting Input')
    numToSend = str(input())
    print(numToSend)
    uart1.write(numToSend)
    print('Sent')
    utime.sleep(5)
