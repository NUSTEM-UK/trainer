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

# Set the display backlight to 100%
display.set_backlight(1)

# Borrowed from Tony Goodhew's PicoDisplay example code
up_arrow =[0,4,14,21,4,4,0,0]
down_arrow = [0,4,4,21,14,4,0,0]
bits = [128,64,32,16,8,4,2,1]  # Powers of 2

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

# set the 4 servo extremeties
s1_1 = 0
s1_2 = 180
s2_1 = 0
s2_2 = 180 

def backround_draw(top_left, top_right, bottom_left, bottom_right):
    display.set_pen(255,255,0)
    display.text(str(top_left), 10, 25,200)
    display.text(str(top_right), 200, 25,200)
    display.text(str(bottom_left), 10, 100,200)
    display.text(str(bottom_right), 200, 100,200)
    #Draw the Top Horizontal Scale
    display.set_pen(255,255,255)
    display.pixel_span(50,31,140)
    display.pixel_span(50,32,140)
    display.pixel_span(50,105,140)
    display.pixel_span(50,106,140)

def draw_ticks(top_left, top_right, bottom_left, bottom_right):
    display.set_pen(255,255,255)
    display.rectangle(top_left, 27, 2, 12)
    display.rectangle(top_right, 27, 2, 12)
    display.rectangle(bottom_left, 100, 2, 12)
    display.rectangle(bottom_right, 100, 2, 12)

while True:
    # print("ello")
    for i in range(top_absolutes[0], top_absolutes[1]-4):
        display.set_pen(0, 0, 0)
        display.clear()
        backround_draw()
        draw_ticks(top_absolutes[0], top_absolutes[1], bottom_absolutes[0], bottom_absolutes[1])       
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
        draw_ticks(top_absolutes[0], top_absolutes[1], bottom_absolutes[0], bottom_absolutes[1]) 
        display.set_pen(255,0,0) # Red Arrows
        draw_char(i, 38, up_arrow)
        draw_char(189-i, 88, down_arrow) # bit wrong

        display.update()