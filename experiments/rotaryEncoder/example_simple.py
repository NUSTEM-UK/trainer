# The MIT License (MIT)
# Copyright (c) 2021 Mike Teachman
# https://opensource.org/licenses/MIT

# example for MicroPython rotary encoder
# Borrowed from https://github.com/miketeachman/micropython-rotary

# Simplified imports, we don't need the guards in our use case
from rotary_irq_rp2 import RotaryIRQ
import time

# Create RotaryIQQ object with half_step set so we increment on each click
# RANGE_BOUNDED limits end-points to 0/180, which we want for servos but
# may need to handle differently for LEDs.
# TODO: work out range limits
r = RotaryIRQ(pin_num_clk=13,
              pin_num_dt=14,
              min_val=0,
              max_val=180,
              reverse=False,
              range_mode=RotaryIRQ.RANGE_BOUNDED,
              pull_up=False,
              half_step=True)

val_old = r.value()
print('>>> Start')
print('result =', val_old)

while True:
    val_new = r.value()

    if val_old != val_new:
        val_old = val_new
        print('result =', val_new)

    time.sleep_ms(50)
