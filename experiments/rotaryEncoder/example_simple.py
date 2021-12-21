# The MIT License (MIT)
# Copyright (c) 2021 Mike Teachman
# https://opensource.org/licenses/MIT

# example for MicroPython rotary encoder
# Borrowed from https://github.com/miketeachman/micropython-rotary

# Simplified imports, we don't need the guards in our use case
from rotary_irq_rp2 import RotaryIRQ
import time
from machine import Pin

# Create RotaryIQQ object with half_step set so we increment on each click
# RANGE_BOUNDED limits end-points to 0/180, which we want for servos but
# may need to handle differently for LEDs.
# TODO: work out range limits
r = RotaryIRQ(pin_num_clk=21,
              pin_num_dt=22,
              min_val=0,
              max_val=180,
              reverse=False,
              range_mode=RotaryIRQ.RANGE_BOUNDED,
              pull_up=False,
              half_step=True)

# Turns out the rotary encoder button shorts to ground when pressed,
# so we need to set the input PULL_UP, and test for no value.
button = Pin(12, Pin.IN, Pin.PULL_UP)

val_old = r.value()
print('>>> Start')
print('result =', val_old)

while True:
    val_new = r.value()

    if val_old != val_new:
        val_old = val_new
        print('result =', val_new)

    # If not because 'pressed' is GND.
    # TODO: debounce handling, via a state toggle on press/release
    if not button.value():
        print('>>> pressed')

    time.sleep_ms(10)
    time.sleep_ms(50)
