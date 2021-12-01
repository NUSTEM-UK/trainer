# UART1 on pins GP4/5 RX/TX

from machine import UART, Pin
import utime

# self.uart = UART(uartNum, 9600, parity=None, stop=1, bits=8, rx=rxPin, tx=txPin)
uart1 = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

while True:
    uart1.write('hello\r')
    print('hello')
    utime.sleep(1)
    uart1.write('world\r')
    print('world')
    utime.sleep(1)
    uart1.write('Hello, world!\r')
    print('Hello, world!')
    utime.sleep(1)
    uart1.write('cabbage\r')
    print('cabbage')
    utime.sleep(1)
