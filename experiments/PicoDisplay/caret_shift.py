import machine
import utime
import gc

# Pico Display boilerplate
import picodisplay as display

width = display.get_width()
height = display.get_height()
gc.collect()
display_buffer = bytearray(width * height * 2)
display.init(display_buffer)

# Set the display backlight to 50%
display.set_backlight(1)

# fills the screen with black
def up_arrow(across, up):
    y=up
    x=across
    display.set_pen(255,255,255)
    display.pixel(x,y)
    display.pixel(x,y-1)
    display.pixel(x+1,y-2)
    display.pixel(x+1,y-3)
    display.pixel(x+2,y-4)
    display.pixel(x+2,y-5)
    display.pixel(x+3,y-5)
    display.pixel(x+3,y-4)
    display.pixel(x+4,y-3)
    display.pixel(x+4,y-2)
    display.pixel(x+5,y-1)
    display.pixel(x+5,y)

def backround_draw():
    display.set_pen(255,255,255)
    display.text("000", 10, 25,200)
    display.text("180", 200, 25,200)
    #display.text("000", 10, 100,200)
    #Draw the Top Horizontal Scale
    display.pixel_span(50,31,140)
    display.pixel_span(50,32,140)

def draw_topticks(left, right):
    first_tick = int(50 + ((left/180)*140))
    second_tick = int(50 + ((right/180)*140))

while True:
    for i in range(51,189):
        display.set_pen(0, 0, 0)
        display.clear()
        backround_draw()
        up_arrow(i,45)
        utime.sleep(0.02)
        display.update()
    for i in range(189,51, -1):
        display.set_pen(0, 0, 0)
        display.clear()
        backround_draw()
        up_arrow(i,45)
        utime.sleep(0.02)
        display.update()