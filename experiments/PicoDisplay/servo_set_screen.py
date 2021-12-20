import picodisplay as display
import utime

# Set up and initialise Pico Display
buf = bytearray(display.get_width() * display.get_height() * 2)
display.init(buf)
display.set_backlight(0.8)
angle = 0

while True:
    display.set_pen(40, 40, 40)
    display.clear()
    display.set_pen(255, 255, 255)
    display.text("Set your angle", 15,15,200,3)
    if angle > 10:
        angle = 0
    display.text(str(angle), 120,70,0,7)
    display.update()
    angle = angle + 1
    utime.sleep(1)

