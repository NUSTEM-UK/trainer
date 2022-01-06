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
    """Wait for serial connection and process handshake

    Sends periodic 'ACK', waiting for an 'ACK ACK ACK' response.
    Sets flag isHarbinger on successful handshake, and unsets
    waitingForConnection.
    """
    global waitingForConnection
    global isHarbinger

    # We've been called, so assume we're not connected
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
    """Not necessarily written in the cleanest way for integration with Joe's work.

    I think what I'd do is:
    - Rewrite getConnection() as a checkForConnection() function, removing the loop from it
    - Have getConnection read serial responses, but send its ACK query only on a time-since-last-called basis
    - Note that serial read handles entire lines, so the existing code will probably work.
    - In __main__, do something like:

        while True:
            if waitingForConnection:
                checkSerialConnection()
            # could probably be a plain else here, since we should be in one state or the other
            if isHarbinger:
                # Code as below, likely abstracted into a function
            # Then whatever's needed for Joe's bit.
            handleButtons()
            updateDisplayAndServoData()
            # ...or whatever

    TODO: Would be nice if the system reverted to waitingForConnection if it's disconnected.
          However, I'm not sure how we'd do that without constantly checking we still have
          a connection... which the Arduino end doesn't currently handle. Which I think means
          both ends of the serial connection will need to be restarted after a session.
          Lack of reset button on a Pico is annoying here.
    """
    while True:
        getConnection()
        while isHarbinger:
            # uart1.write(str(servo1pos) + ',' + str(servo2pos) + '\n')
            # Pad strings we send so we get expected number of digits
            uart1.write(f'{servo1pos:03}' + ',' + f'{servo2pos:03}' + '\n')
            # print(servo1pos, servo2pos)
            print(f'{servo1pos:03}' + ',' + f'{servo2pos:03}')
            servo1pos = (servo1pos + 5) % 180
            servo2pos = (servo2pos - 5) % 180
            utime.sleep(delayShort)
            # In principle we could poll here for some sort
            # of response, and set isHarbinger to False if it's
            # not found for some time. Then we'd fall back around
            # the loop and be polling for a connection again.
