# UART1 on pins GP4/5 RX/TX

from machine import UART, Pin
import utime

# self.uart = UART(uartNum, 9600, parity=None, stop=1, bits=8, rx=rxPin, tx=txPin)
uart1 = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
delay = 0.25

while True:
    uart1.write('hello\n')
    print('hello')
    utime.sleep(delay)
    uart1.write('world\n')
    print('world')
    utime.sleep(delay)
    uart1.write('Hello, world!\n')
    print('Hello, world!')
    utime.sleep(delay)
    uart1.write('cabbage\n')
    print('cabbage')
    utime.sleep(delay)
