# Quick test of Pico-Go. Should flash the built-in LED
from machine import Pin
import time

pin = Pin(25, Pin.OUT)

while True:
    pin.toggle()
    time.sleep_ms(1000)
