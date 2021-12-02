import machine
import utime
import gc

# Pico Display boilerplate
import picodisplay as display

width = display.get_width()
height = display.get_height()
gc.collect()
display_buffer = bytearray(width * height * 2)
# Fill with black
display.init(display_buffer)

# Set the display backlight to 50%
display.set_backlight(1)

# Borrowed from Tony Goodhew's PicoDisplay example code
up_arrow =[0,4,14,21,4,4,0,0]
down_arrow = [0,4,4,21,14,4,0,0]
bits = [128,64,32,16,8,4,2,1]  # Powers of 2

# Awkward bit where I test out the limiter for the motion
# These are angles between 0 and 180
top_interval = [1, 120] 
bottom_interval = [20, 170]
top_absolutes = (int(50 + ((top_interval[0]/180)*140)), int(50 + ((top_interval[1]/180)*140)))

print(top_absolutes)

# Print defined character from set above
def draw_char(xpos, ypos, pattern):
    for line in range(8):  # 5x8 characters
        for ii in range(5): # Low value bits only
            i = ii + 3
            dot = pattern[line] & bits[i] # Extract bit
            if dot: # print white dots
                display.pixel(xpos+i*2, ypos+line*2)
                display.pixel(xpos+i*2, ypos+line*2+1)
                display.pixel(xpos+i*2+1, ypos+line*2)
                display.pixel(xpos+i*2+1, ypos+line*2+1)

def draw_up_arrow(across, up):
    # Replaced with draw_char, above
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
    display.set_pen(255,255,0)
    display.text("000", 10, 25,200)
    display.text("180", 200, 25,200)
    display.text("000", 10, 100,200)
    display.text("180", 200, 100,200)
    #Draw the Top Horizontal Scale
    display.set_pen(255,255,255)
    display.pixel_span(50,31,140)
    display.pixel_span(50,32,140)
    display.pixel_span(50,105,140)
    display.pixel_span(50,106,140)

def draw_topticks(left, right):
    # left = 80
    # right = 100
    first_tick = left
    second_tick = right
    display.set_pen(255,255,255)
    display.rectangle(first_tick, 27, 2, 6)
    display.rectangle(second_tick, 27, 2, 6)

# def draw_lowticks(left, right):
#     first_tick = int(50 + ((left/180)*140))
#     second_tick = int(50 + ((right/180)*140))

while True:
    # print("ello")
    for i in range(top_absolutes[0], top_absolutes[1]-4):
        display.set_pen(0, 0, 0)
        display.clear()
        backround_draw()
        draw_topticks(top_absolutes[0], top_absolutes[1])
        display.set_pen(255,0,0) # Red Arrows
        draw_char(i, 38, up_arrow)
        draw_char(189-i, 88, down_arrow)
        # draw_up_arrow(i,45)
        # draw_up_arrow(i,100)
        # utime.sleep(0.002)
        display.update()
    for i in range(top_absolutes[1]-4,top_absolutes[0], -1): # -4 adjusts for caret arrow widths
        display.set_pen(0, 0, 0)
        display.clear()
        backround_draw()
        draw_topticks(top_absolutes[0], top_absolutes[1])
        display.set_pen(255,0,0) # Red Arrows
        draw_char(i, 38, up_arrow)
        draw_char(189-i, 88, down_arrow) # bit wrong
        # draw_up_arrow(i,45)
        # draw_up_arrow(i,100)
        # utime.sleep(0.002)
        display.update()
