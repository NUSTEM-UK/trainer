import picodisplay as display
import utime

# Set up and initialise Pico Display
buf = bytearray(display.get_width() * display.get_height() * 2)
display.init(buf)
display.set_backlight(0.8)

# set the cycle transition time in ms
wait_cycle_time = 2000
circle_rad_min = 6
circle_rad_max = 20

in_circle_min = 4
in_circle_max = 18

# define inital start and end times
start_time = utime.ticks_ms()
end_time = start_time + wait_cycle_time
now_time = start_time 

def wait_screen():
    global start_time
    global end_time
    global now_time

    # get the current time
    now_time = utime.ticks_ms()

    # now_time as a proportion of the total cycle time
    done_so_far = (now_time - start_time)/(end_time - start_time)
    if done_so_far < 0.5:
        #going up
        current_radius = circle_rad_min + (done_so_far * 2 * (circle_rad_max - circle_rad_min))
        current_in_radius = in_circle_min + (done_so_far * 2 * (in_circle_max - in_circle_min))
    elif 1.0 >= done_so_far >= 0.5:
        # we back the way down
        done_so_far = 1 - done_so_far
        current_radius = circle_rad_min + (done_so_far * 2 * (circle_rad_max - circle_rad_min))
        current_in_radius = in_circle_min + (done_so_far * 2 * (in_circle_max - in_circle_min))
    else:        
        start_time = now_time
        end_time = start_time + wait_cycle_time
        current_radius = circle_rad_min
        current_in_radius = in_circle_min

    # clear the background
    display.set_pen(0, 0, 0)
    display.clear()

    # Draw text
    display.set_pen(255,255,255)
    display.text("Waiting for connection...", 30, 25, 200)
    
    # Draw text
    display.set_pen(0,255,50)
    display.circle(125,90,int(current_radius))
    display.set_pen(0,0,0)
    display.circle(125,90,int(current_in_radius))
    display.update()

while True:
    wait_screen()
    utime.sleep_ms(10)