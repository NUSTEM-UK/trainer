import picodisplay as display
import utime

# Initialise display with a bytearray display buffer
buf = bytearray(display.get_width() * display.get_height() * 2)
display.init(buf)
display.set_backlight(0.5)

# sets up a handy function we can call to clear the screen
def clear():
    display.set_pen(0, 0, 0)
    display.clear()
    display.update()

while True:
    while display.is_pressed(BUTTON_A):
        print("A Is Pressed")
    print("Nothing is Pressed")