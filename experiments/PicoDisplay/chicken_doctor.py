from machine import UART, Pin
import picodisplay as display
import utime

# Need to upload rotary_irq_rp2.py and rotary.py to the pico
from rotary_irq_rp2 import RotaryIRQ

# Create Rotary object
r = RotaryIRQ(pin_num_clk=21,
              pin_num_dt=22,
              min_val=-5000,
              max_val=+5000,
              reverse=False,
              range_mode=RotaryIRQ.RANGE_WRAP, # set wrap, as range starts at min_val
              pull_up=False,
              half_step=True)

val_old = r.value()
val_new = r.value()

# Configure UART serial connection

uart1 = UART(1, baudrate=57600, tx=Pin(4), rx=Pin(5))
serial_delay = 0.5
serial_delay_short = 0.1

waiting_for_connection = True
is_connected = False

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

    # colours chosen depending on which button has been pressed
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
servo1_x_start = 0
servo1_x_current = servo1_x_start
servo1_x_end = 180

servo2_x_start = 0
servo2_x_current = servo2_x_start
servo2_x_end = 180

current_angle_top = 0
current_angle_bottom = 0

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

# rotary debounce timer
rotary_moved = utime.ticks_ms()
rotary_wait = 60        # debounce in ms

# set serial connection flags
waiting_for_connection = True
is_connected = False

# update function - how long has passed since last update, and where should we be now
def update_animation():
    global current_angle_top
    global current_angle_bottom
    display.set_pen(0, 0, 0)
    display.clear()
    global start_time
    global end_time
    global now_time

    global servo1_x_start
    global servo1_x_end

    global servo2_x_start
    global servo2_x_end

    # get the current time
    now_time = utime.ticks_ms()

    # now_time as a proportion of the total cycle time
    done_so_far = (now_time - start_time)/(end_time - start_time)

    # are we on the way up, or headed back down
    if done_so_far < 0.5:
        # we're on the way up, as 1.0 would be a full cycle
        # use that proportion to work out where we should be angularly
        current_angle_top = servo1_x_start + (done_so_far * 2 * (servo1_x_end - servo1_x_start))
        current_angle_bottom = servo2_x_start + (done_so_far * 2 * (servo2_x_end - servo2_x_start))
        # then use the angle to work out the pixl position of where we are
        current_pixel_top = int(x_min + (current_angle_top / x_angle_max) * (x_max - x_min))
        current_pixel_bottom = int(x_min + (current_angle_bottom / x_angle_max) * (x_max - x_min))

    elif 1.0 >= done_so_far >= 0.5:
        # we back the way down
        done_so_far = 1 - done_so_far

        current_angle_top = servo1_x_start + (done_so_far * 2 * (servo1_x_end - servo1_x_start))
        current_angle_bottom = servo2_x_start + (done_so_far * 2 * (servo2_x_end - servo2_x_start))
        # then use the angle to work out the pixl position of where we are
        current_pixel_top = int(x_min + (current_angle_top / x_angle_max) * (x_max - x_min))
        current_pixel_bottom = int(x_min + (current_angle_bottom / x_angle_max) * (x_max - x_min))
    else:
        # we've completed the cycle, so set new start and end times
        start_time = now_time
        end_time = start_time + cycle_time
        current_angle_top = servo1_x_start
        current_angle_bottom = servo2_x_start
        current_pixel_top = int(x_min + (current_angle_top / x_angle_max) * (x_max - x_min))
        current_pixel_bottom = int(x_min + (current_angle_bottom / x_angle_max) * (x_max - x_min))

    backround_draw(servo1_x_start, servo1_x_end, servo2_x_start, servo2_x_end)
    display.set_pen(255, 0, 0)
    draw_char(current_pixel_top-6, 38, up_arrow)
    draw_char(current_pixel_bottom-6, 88, down_arrow)

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

def rotary_checker():
    global button_a
    global button_b
    global button_x
    global button_y

    global servo1_x_start
    global servo1_x_end

    global servo2_x_start
    global servo2_x_end

    global rotary_moved

    global val_new
    global val_old

    total = button_y + button_x + button_a + button_b

    if total > 0 and (utime.ticks_ms() - rotary_moved) > 30:
        rotary_moved = utime.ticks_ms()
        val_new = r.value()
        if button_a > 0:
            if val_new > val_old:
                if servo1_x_start < servo1_x_end and servo1_x_start >= 0:
                    servo1_x_start = servo1_x_start + 1
                val_old = val_new
            elif val_new < val_old:
                if servo1_x_start <= servo1_x_end and servo1_x_start > 0:
                    servo1_x_start = servo1_x_start - 1
                val_old = val_new
        elif button_x > 0:
            if val_new > val_old:
                if servo1_x_start <= servo1_x_end and servo1_x_end < 180:
                    servo1_x_end = servo1_x_end + 1
                val_old = val_new
            elif val_new < val_old:
                if servo1_x_start < servo1_x_end and servo1_x_end <= 180:
                    servo1_x_end = servo1_x_end - 1
                val_old = val_new
        elif button_b > 0:
            if val_new > val_old:
                if servo2_x_start < servo2_x_end and servo2_x_start >= 0:
                    servo2_x_start = servo2_x_start + 1
                val_old = val_new
            elif val_new < val_old:
                if servo2_x_start <= servo2_x_end and servo2_x_start > 0:
                    servo2_x_start = servo2_x_start - 1
                val_old = val_new
        else:
            if val_new > val_old:
                if servo2_x_start <= servo2_x_end and servo2_x_end < 180:
                    servo2_x_end = servo2_x_end + 1
                val_old = val_new
            elif val_new < val_old:
                if servo2_x_start < servo2_x_end and servo2_x_end <= 180:
                    servo2_x_end = servo2_x_end - 1
                val_old = val_new

def connection_checker():
    global waiting_for_connection
    global is_connected
    global current_angle_top
    global current_angle_bottom

    if waiting_for_connection:
        uart1.write('ACK\n')
        print("ACK")
        print("Checking for response...")
        if uart1.any() > 0:
            received = uart1.read().decode()
            print("response received")
            print(received)
            if received == "ACK ACK ACK":
                print('RESPONDED:' + received)
                print('>>> ASSUMING DIRECT CONTROL <<<')
                utime.sleep(serial_delay)
                print('>>> I HAVE CONTROL <<<')
                is_connected = True
                waiting_for_connection = False
        # if we haven't had any response, pause briefly and exit
        utime.sleep(serial_delay)


if __name__ == '__main__':
    while True:
        # while waiting_for_connection:
        button_checker()
        rotary_checker()
        update_animation()
        if is_connected:
            # Pad strings we send so we get expected number of digits
            uart1.write(f'{current_angle_top:03}' + ',' + f'{current_angle_bottom:03}' + '\n')
            # print(servo1pos, servo2pos)
            print(f'{current_angle_top:03}' + ',' + f'{current_angle_bottom:03}')

            # In principle we could poll here for some sort
            # of response, and set is_connected to False if it's
            # not found for some time. Then next pass we'd fall into
            # the else block below, and go back to looking for a connection.
        else:
            connection_checker()

        utime.sleep_ms(100)

