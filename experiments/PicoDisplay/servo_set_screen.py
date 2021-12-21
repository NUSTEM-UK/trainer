import picodisplay as display
from rotary_irq_rp2 import RotaryIRQ
import utime
import time
from machine import Pin

# Set up and initialise Pico Display
buf = bytearray(display.get_width() * display.get_height() * 2)
display.init(buf)
display.set_backlight(0.8)
angle = 0

# Rotary Encoder connection details
# need rotary_irq_rp2.py and rotary.py saved to the Pico
# VCLICK --> GP21, DT --> GP22
# Note + needs to go to 3V3 and not 3v3EN


# Create Rotary object
r = RotaryIRQ(pin_num_clk=21,
              pin_num_dt=22,
              min_val=0,
              max_val=180,
              reverse=False,
              range_mode=RotaryIRQ.RANGE_BOUNDED,
              pull_up=False,
              half_step=True)

val_old = r.value()

while True:
    display.set_pen(40, 40, 40)
    display.clear()
    display.set_pen(255, 255, 255)
    display.text("Set your angle", 15,15,200,3)

    # Get the data from the encoder
    val_new = r.value()

    if val_old != val_new:
        val_old = val_new
        #print('result =', val_new)

    display.text(str(val_old), 120,70,0,7)
    display.update()

    time.sleep_ms(10)
    time.sleep_ms(50)

