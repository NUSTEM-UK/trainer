# UART1 on pins GP4/5 RX/TX

from machine import UART, Pin
import utime

# self.uart = UART(uartNum, 9600, parity=None, stop=1, bits=8, rx=rxPin, tx=txPin)
uart1 = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
delay = 1

servo1pos = 0
servo2pos = 180

waitingForConnection = True
harbingerMode = False

# uart1.write('hello\n')
# print('hello')
# utime.sleep(delay)
# uart1.write('world\n')
# print('world')
# utime.sleep(delay)
# uart1.write('Hello, world!\n')
# print('Hello, world!')
# utime.sleep(delay)

while True:
    if uart1.any() > 0:
        #received = uart1.read(2)
        received = uart1.read()
        decoded = received.decode()
        print(decoded)
        if decoded == '80':
            print("DING!")

# while waitingForConnection:
#     uart1.write('ACK\n')
#     print("ACK")

#     print("Waiting for response...")
#     if uart1.any() > 0:
#         received = uart1.read(12)
#         print("response received")
#         print(received)
#         if received == "ACK ACK ACK\n":
#             print('RESPONDED:' + received)
#             print('>>> ASSUMING DIRECT CONTROL <<<')
#             harbingerMode = True
#             waitingForConnection = False
#     utime.sleep(delay)

# while harbingerMode:
#     uart1.write(str(servo1pos) + ' ' + str(servo2pos) + '\n')
#     utime.sleep(delay)

