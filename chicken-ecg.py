from machine import UART, Pin
import picodisplay as display
import utime
# from picofont import cmap, printchar, printstring
# Need to upload rotary_irq_rp2.py and rotary.py to the Pico
from rotary_irq_rp2 import RotaryIRQ

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


def rescale(x, in_min, in_max, out_min, out_max):
    """Rescale a value from one range to another."""
    # Check for range zero
    if in_max - in_min == 0:
        print("RESCALE: Caught a divide by zero.")
        return out_min
    else:
        return int( out_min + ((x - in_min) * (out_max - out_min) / (in_max - in_min)) )


def zfl(s, width):
    """Pads string with leading zeros.

    From https://stackoverflow.com/questions/63271522/is-there-a-zfill-type-function-in-micro-python-zfill-in-micro-python
    There's no zfill() in Micropython."""
    return '{:0>{w}}'.format(s, w=width)


def connection_check():
    global waiting_for_connection
    global is_connected
    global serial_delay

    if waiting_for_connection:
        uart1.write('ACK\n')
        print("ACK")
        print("Checking for response...")
        if uart1.any() > 0:
            # FIXME: Wrap this is a try/catch, it can error out and cause a crash.
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

class ServoController:
    """Visual and serial interface for servo control.
    """

    def __init__(self, angle=90, speed=20, vertical_offset=25, marker=up_arrow, marker_offset=0):
        """Initialise the controller, with vaguely sane defaults."""
        self.angle = angle
        self.speed = speed
        self.vertical_offset = vertical_offset
        self.marker = marker
        self.marker_offset = marker_offset

        # TODO: I don't think @property/getter/setter decorators work
        #       in Micropython, so it's a pain to do input validation.
        #       But equally, I can't find any documentation on this. Sigh.

        self.min_angle = 0
        self.max_angle = 180

        self._min_display_position = 0
        self._max_display_position = 180

        self._reversing = False

        # Booleans to determine pen colour for drawing values
        self.min_position_being_updated = False
        self.max_position_being_updated = False
        self.position_being_updated = False
        self.speed_being_updated = False
        self.is_selected = False

        # Set a time reference
        self._time_ref = utime.ticks_ms()

    def draw(self):
        """Draw the servo on the display."""

        # Are we selected? if so, draw a background
        if self.is_selected:
            display.set_pen(70, 70, 70)
            display.rectangle(0, self.vertical_offset - 20, 240, self.vertical_offset + 20)

        # Display minimum angle
        # Set pen colour to green if being updated, else yellow
        display.set_pen(0, 255, 0) if self.min_position_being_updated else display.set_pen(255, 255, 0)
        display.text(zfl(str(self.min_angle), 3), 10, self.vertical_offset, 200)
        # printstring(zfl(str(self.min_angle), 3), 10, self.vertical_offset, 1, False, False)

        # Display maximum angle
        display.set_pen(0, 255, 0) if self.max_position_being_updated else display.set_pen(255, 255, 0)
        display.text(zfl(str(self.max_angle), 3), 200, self.vertical_offset, 200)

        # Draw scale line
        display.set_pen(255, 255, 255)
        display.rectangle(50, self.vertical_offset + 6, 140, 2)
        # display.pixel_span(50, self.vertical_offset + 6, 140)
        # display.pixel_span(50, self.vertical_offset + 7, 140)
        # display.update()

        # Draw movement end tic marks
        self._tick_min = rescale(self.min_angle, 0, 180, 50, 140 + 50)
        x = rescale
        self._tick_max = rescale(self.max_angle, 0, 180, 50, 140 + 50)
        display.rectangle(self._tick_min, self.vertical_offset + 2, 2, 10)
        display.rectangle(self._tick_max, self.vertical_offset + 2, 2, 10)

        # Draw position marker
        self._marker_pos = rescale(self.angle, 0, 180, 50, 140 + 50) - 10
        display.set_pen(255, 0, 0)
        draw_char(self._marker_pos, self.vertical_offset + 13 + self.marker_offset, self.marker)

    def min_position_setting_toggle(self):
        self.min_position_being_updated = not self.min_position_being_updated
        # Deselect the other thing if appropriate
        if self.min_position_being_updated:
            self.max_position_being_updated = False

    def max_position_setting_toggle(self):
        self.max_position_being_updated = not self.max_position_being_updated
        # Deselect the other thing if appropriate
        if self.max_position_being_updated:
            self.min_position_being_updated = False

    def increment_value(self):
        """Increment whatever we're incrementing.

        Keep it within bounds.
        """
        # print(">>> Incrementing")
        if self.min_position_being_updated:
            self.min_angle += 1
        if self.min_angle > 180:
            self.min_angle = 180

        if self.max_position_being_updated:
            self.max_angle += 1
        if self.max_angle > 180:
            self.max_angle = 180

        # if we're moving min and it's > max, increment max also
        if self.min_angle > self.max_angle:
            self.max_angle = self.min_angle

        # print(f"[{self.min_angle}, {self.max_angle}]")

    def decrement_value(self):
        """Decrement whatever we're decrementing.

        Keep it within bounds.
        """
        if self.min_position_being_updated:
            self.min_angle -= 1
        if self.min_angle < 0:
            self.min_angle = 0

        if self.max_position_being_updated:
            self.max_angle -= 1
        if self.max_angle < 0:
            self.max_angle = 0

        if self.max_angle < self.min_angle:
            self.min_angle = self.max_angle


    def update(self):
        """Update the servo position."""

        # Calculate angular movement since last update
        self._time_delta = utime.ticks_diff(utime.ticks_ms(), self._time_ref)
        self._time_ref = utime.ticks_ms()
        self._angle_delta = self.speed * self._time_delta / 1000

        # Update angular position, catching end points
        if self._reversing:
            self.angle -= self._angle_delta
            if self.angle < self.min_angle:
                self.angle = self.min_angle
                self._reversing = False
        else:
            self.angle += self._angle_delta
            if self.angle > self.max_angle:
                self.angle = self.max_angle
                self._reversing = True


class ButtonController:
    """Poll buttons and dispatch events.

    Takes a mapping dictionary of buttons, objects and method calls.
    Polls the buttons and calls the appropriate method on the object.
    Could instantiate a ButtonController object per menu mode.
    """

    def __init__(self, mapping, debounce_interval=500):
        """Initialise the controller."""
        self._mapping = mapping
        self.debounce_interval = debounce_interval
        self._time_last_checked = utime.ticks_ms()

    def check(self):
        """Check the buttons and call the appropriate method."""
        # Check for button presses
        for button in self._mapping:
            if display.is_pressed(button) and utime.ticks_diff(utime.ticks_ms(), self._time_last_checked) > self.debounce_interval:
                self._time_last_checked = utime.ticks_ms()
                # Have to use getattr here for dynamic method call
                getattr(self._mapping[button]['object'], self._mapping[button]['method'])()


class RotaryController():
    """Read rotary encoder value and dispatch accordingly.

    Takes a mapping dictionary of servo objects and method calls.
    Polls the encoder and calls the appropriate method on the object.
    """

    def __init__(self, mapping, debounce_interval=60):
        """Initialize the controller."""
        self._mapping = mapping
        self._debounce_interval = debounce_interval
        self._time_last_checked = utime.ticks_ms()

        self._r = RotaryIRQ(pin_num_clk=21,
              pin_num_dt=22,
              min_val=-5000,
              max_val=+5000,
              reverse=False,
              range_mode=RotaryIRQ.RANGE_WRAP, # set wrap, as range starts at min_val
              pull_up=False,
              half_step=True)

        self._old_value = self._r.value()
        self._new_value = self._r.value()

    def check(self):
        """Check the rotary encoder value and dispatch accordingly."""

        if utime.ticks_diff(utime.ticks_ms(), self._time_last_checked) > self._debounce_interval:
            self._time_last_checked = utime.ticks_ms()
            self._new_value = self._r.value()
            if self._new_value > self._old_value:
                self._old_value = self._new_value
                for object in self._mapping:
                    getattr(object, self._mapping[object]['inc_method'])()
                    # print("Incrementing")
                    # print(object, self._mapping[object]['inc_method'])
            if self._new_value < self._old_value:
                self._old_value = self._new_value
                for object in self._mapping:
                    # Note the (): you still have to call the method once you've found it.
                    getattr(object, self._mapping[object]['dec_method'])()
                    # print("Decrementing")


if __name__ == '__main__':
    print("Starting...")

    servoD5 = ServoController()
    servoD5.angle = 90
    print(servoD5.angle)
    servoD5.angle = 180
    print(servoD5.angle)
    servoD5.angle = 200
    print(servoD5.angle)

    servoD7 = ServoController(speed=60, vertical_offset=90, marker=down_arrow, marker_offset=-25)

    # For some reason, we need to draw everything once, or the methods error out in the loop. weird.
    display.set_pen(0, 0, 0)
    display.clear()
    servoD5.draw()
    servoD7.draw()
    display.update()

    # Setting up callbacks for buttons and rotary encoder.
    # This is for the main screen: later modes will pass their own sets here.
    button_mapping = {
        display.BUTTON_A: {
            "object": servoD5, "method": "min_position_setting_toggle" },
        display.BUTTON_X: {
            "object": servoD5, "method": "max_position_setting_toggle" },
        display.BUTTON_B: {
            "object": servoD7, "method": "min_position_setting_toggle" },
        display.BUTTON_Y: {
            "object": servoD7, "method": "max_position_setting_toggle" }
    }
    buttons = ButtonController(button_mapping, debounce_interval=500)

    rotary_mapping = {
        servoD5: {
            "inc_method": "increment_value",
            "dec_method": "decrement_value"
        },
        servoD7: {
            "inc_method": "increment_value",
            "dec_method": "decrement_value"
        }
    }
    rotary = RotaryController(rotary_mapping)

    while True:
        display.set_pen(0, 0, 0)
        display.clear()
        servoD5.draw()
        servoD7.draw()
        display.update()

        servoD5.update()
        servoD7.update()

        buttons.check()
        rotary.check()

        # Handle serial stuff
        if is_connected:
            send_string = f'{int(servoD5.angle):03}' + ',' + f'{int(servoD7.angle):03}'
            # print(send_string)
            uart1.write(send_string + '\n')
        else:
            connection_check()

        utime.sleep_ms(20)

