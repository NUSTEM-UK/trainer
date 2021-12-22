# UART1 on pins GP4/5 RX/TX

from machine import UART, Pin
import utime

# self.uart = UART(uartNum, 9600, parity=None, stop=1, bits=8, rx=rxPin, tx=txPin)
uart1 = UART(1, baudrate=57600, tx=Pin(4), rx=Pin(5))
delay = 1
delayShort = 0.1

servo1pos = 0
servo2pos = 180

waitingForConnection = True
isHarbinger = False # It's a Mass Effect reference

def getConnection():
    global waitingForConnection
    global isHarbinger
    while waitingForConnection:
        uart1.write('ACK\n')
        print("ACK")

        print("Waiting for response...")
        if uart1.any() > 0:
            received = uart1.read().decode()
            print("response received")
            print(received)
            if received == "ACK ACK ACK":
                print('RESPONDED:' + received)
                print('>>> ASSUMING DIRECT CONTROL <<<')
                utime.sleep(1)
                print('>>> I HAVE CONTROL <<<')
                isHarbinger = True
                waitingForConnection = False
        utime.sleep(delay)

if __name__ == '__main__':
    while True:
        getConnection()
        while isHarbinger:
            # uart1.write(str(servo1pos) + ',' + str(servo2pos) + '\n')
            # Pad strings we send so we get expected number of digits
            uart1.write(f'{servo1pos:03}' + ',' + f'{servo2pos:03}' + '\n')
            servo1pos = (servo1pos + 5) % 180
            servo2pos = (servo2pos - 5) % 180
            print(servo1pos, servo2pos)
            utime.sleep(delayShort)
            # In principle we could poll here for some sort
            # of response, and set isHarbinger to False if it's
            # not found for some time. Then we'd fall back around
            # the loop and be polling for a connection again.
