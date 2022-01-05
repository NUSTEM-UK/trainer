import picodisplay as display
import utime
import gc
import machine

# Set up and initialise Pico Display
buf = bytearray(display.get_width() * display.get_height() * 2)
display.init(buf)
display.set_backlight(0.8)

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

def backround_draw(top_left, top_right, bottom_left, bottom_right):
    global button_a
    global button_b
    global button_x
    global button_y

    if button_a == 1:
        display.set_pen(0,255,0)
    else:
        display.set_pen(255,255,0)
    display.text(str(top_left), 10, 25,200)
    
    if button_x == 1:
        display.set_pen(0,255,0)
    else:
        display.set_pen(255,255,0)    
    display.text(str(top_right), 200, 25,200)
    if button_b == 1:
        display.set_pen(0,255,0)
    else:
        display.set_pen(255,255,0)
    display.text(str(bottom_left), 10, 100,200)
    
    if button_y == 1:
        display.set_pen(0,255,0)
    else:
        display.set_pen(255,255,0)    
    display.text(str(bottom_right), 200, 100,200)
    #Draw the Top Horizontal Scale
    display.set_pen(255,255,255)
    display.pixel_span(50,31,140)
    display.pixel_span(50,32,140)
    display.pixel_span(50,105,140)
    display.pixel_span(50,106,140)

    #calculate the pixel positions of the ticks
    top_interval = [top_left, top_right] 
    bottom_interval = [bottom_left, bottom_right]

    top_absolutes = (int(50 + ((top_interval[0]/180)*140)), int(50 + ((top_interval[1]/180)*140)))
    bottom_absolutes = (int(50 + ((bottom_interval[0]/180)*140)), int(50 + ((bottom_interval[1]/180)*140)))

    display.set_pen(255,255,255)
    display.rectangle(top_absolutes[0], 27, 2, 12)
    display.rectangle(top_absolutes[1], 27, 2, 12)
    display.rectangle(bottom_absolutes[0], 100, 2, 12)
    display.rectangle(bottom_absolutes[1], 100, 2, 12)

# set the min and max x pixel positions
x_min = 50
x_max = 180

# set the min and max x angular positions
x_angle_min = 0
x_angle_max = 180

# set the cycle transition time in ms
cycle_time = 5000

# set default angles for for the two servos - default swing between 0 and 180
servo1_x_start = 30
servo1_x_current = servo1_x_start
servo1_x_end = 100

servo2_x_start = 0
servo2_x_current = servo2_x_start
servo2_x_end = 180

# define inital start and end times
start_time = utime.ticks_ms()
end_time = start_time + cycle_time
now_time = start_time 

# set flags for button pressing
button_a = 0
button_x = 0
button_b = 0
button_y = 0

# button timer
button_pressed = utime.ticks_ms()
button_wait = 500


print (start_time)
print (end_time)

# update function - how long has passed since last update, and where should we be now
def update_animation():
    display.set_pen(0, 0, 0)
    display.clear()
    global start_time
    global end_time
    global now_time
    # get the current time
    now_time = utime.ticks_ms()

    # now_time as a proportion of the total cycle time
    done_so_far = (now_time - start_time)/(end_time - start_time)

    # are we on the way up, or headed back down 

    if done_so_far < 0.5:
        # we're on the way up, as 1.0 would be a full cycle
        # use that proportion to work out where we should be angularly
        current_angle = servo1_x_start + (done_so_far * 2 * (servo1_x_end - servo1_x_start))

        # then use the angle to work out the pixl position of where we are
        current_pixel = int(x_min + (current_angle / x_angle_max) * (x_max - x_min))

    elif 1.0 >= done_so_far >= 0.5:
        # we back the way down
        done_so_far = 1 - done_so_far

        current_angle = servo1_x_start + (done_so_far * 2 * (servo1_x_end - servo1_x_start))

        # then use the angle to work out the pixl position of where we are
        current_pixel = int(x_min + (current_angle / x_angle_max) * (x_max - x_min))
    else:
        # we've completed the cycle, so set new start and end times
        start_time = now_time
        end_time = start_time + cycle_time
        current_angle = servo1_x_start
        current_pixel = int(x_min + (current_angle / x_angle_max) * (x_max - x_min))
    backround_draw(servo1_x_start, servo1_x_end, servo2_x_start, servo2_x_end)
    draw_char(current_pixel-6, 38, up_arrow)

    display.update()

def button_checker():
    global button_a
    global button_b
    global button_x
    global button_y
    global button_pressed

    total = button_y + button_x + button_a + button_b

    if (utime.ticks_ms() - button_pressed) > 500:
        if display.is_pressed(display.BUTTON_A):
            if button_a == 1:
                button_a = 0
            elif button_b == 1 or button_y == 1 or button_x == 1:
                button_a = 1
                button_b = 0
                button_x = 0
                button_y = 0
                print("A pressed") 
            else:
                button_a = 1
            button_pressed = utime.ticks_ms()
        
        if display.is_pressed(display.BUTTON_B):              # if a button press is detected then...   
            if button_b == 1:
                button_b = 0
            elif button_a == 1 or button_y == 1 or button_x == 1:
                button_a = 0
                button_b = 1
                button_x = 0
                button_y = 0
                print("B pressed") 
            else:
                button_b = 1
            button_pressed = utime.ticks_ms()

        if display.is_pressed(display.BUTTON_X):              # if a button press is detected then...   
            if button_x == 1:
                button_x = 0
            elif button_b == 1 or button_y == 1 or button_a == 1:
                button_a = 0
                button_b = 0
                button_x = 1
                button_y = 0
                print("X pressed") 
            else:
                button_x = 1
            button_pressed = utime.ticks_ms()
        
        if display.is_pressed(display.BUTTON_Y):              # if a button press is detected then...   
            if button_y == 1:
                button_y = 0
            elif button_b == 1 or button_a == 1 or button_x == 1:
                button_a = 0
                button_b = 0
                button_x = 0
                button_y = 1
                print("Y pressed") 
            else:
                button_y = 1
            button_pressed = utime.ticks_ms()



while True:
    button_checker()
    update_animation()
    utime.sleep_ms(10)

