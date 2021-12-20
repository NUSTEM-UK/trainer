import picodisplay as display
import utime

# Set up and initialise Pico Display
buf = bytearray(display.get_width() * display.get_height() * 2)
display.init(buf)
display.set_backlight(0.8)

# Borrowed from Tony Goodhew's PicoDisplay example code
up_arrow =[0,4,14,21,4,4,0,0]
down_arrow = [0,4,4,21,14,4,0,0]
bits = [128,64,32,16,8,4,2,1]  # Powers of 2

# set the min and max x pixel positions
x_min = 50
x_max = 140

# set the min and max x angular positions
x_angle_min = 0
x_angle_max = 180

# set the cycle transition time in ms
cycle_time = 5000

# set default angles for for the two servos - default swing between 0 and 180
servo1_x_start = 0
servo1_x_current = servo1_x_start
servo1_x_end = 180

servo2_x_start = 0
servo2_x_current = servo2_x_start
servo2_x_end = 180

# define inital start and end times
start_time = utime.ticks_ms()
end_time = start_time + cycle_time
now_time = start_time 

print (start_time)
print (end_time)

# update function - how long has passed since last update, and where should we be now
def update_animation():
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
        print ("Current angle is:", current_angle, sep=' ')

        # then use the angle to work out the pixl position of where we are
        current_pixel = x_min + (current_angle / x_angle_max) * (x_max - x_min)
        print ("Current pixel is:", current_pixel, sep=' ')

    elif 1.0 >= done_so_far >= 0.5:
        # we back the way down
        done_so_far = 1 - done_so_far

        current_angle = servo1_x_start + (done_so_far * 2 * (servo1_x_end - servo1_x_start))
        print ("Current angle is:", current_angle, sep=' ')

        # then use the angle to work out the pixl position of where we are
        current_pixel = x_min + (current_angle / x_angle_max) * (x_max - x_min)
        print ("Current pixel is:", current_pixel, sep=' ')        
    else:
        # we've completed the cycle, so set new start and end times
        start_time = now_time
        end_time = start_time + cycle_time
        print("Cycle Complete")


while True:
    update_animation()
    utime.sleep_ms(100)

