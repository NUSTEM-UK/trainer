from machine import UART, Pin
import picodisplay as display
import utime
# Need to upload rotary_irq_rp2.py and rotary.py to the Pico
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


def rescale(x, in_min, in_max, out_min, out_max):
    """Rescale a value from one range to another."""
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def zfl(s, width):
    """Pads string with leading zeros.

    From https://stackoverflow.com/questions/63271522/is-there-a-zfill-type-function-in-micro-python-zfill-in-micro-python
    There's no zfill() in Micropython."""
    return '{:0>{w}}'.format(s, w=width)

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



if __name__ == '__main__':
    print("Starting")
    servoD5 = ServoController()
    servoD5.angle = 90
    print(servoD5.angle)
    servoD5.angle = 180
    print(servoD5.angle)
    servoD5.angle = 200
    print(servoD5.angle)

    servoD7 = ServoController(speed=60, vertical_offset=90, marker=down_arrow, marker_offset=-25)

    while True:
        display.set_pen(0, 0, 0)
        display.clear()
        servoD5.draw()
        servoD7.draw()
        display.update()
        # servoD7.draw()

        servoD5.update()
        servoD7.update()

