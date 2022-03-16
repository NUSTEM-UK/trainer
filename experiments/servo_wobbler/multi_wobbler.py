import utime
from servo import Servo


def rescale(x, in_min, in_max, out_min, out_max):
    """Rescale a value from one range to another."""
    # print(x, in_min, in_max, out_min, out_max)
    # Check for range zero
    if in_max - in_min == 0:
        print("RESCALE: Caught a divide by zero.")
        return out_min
    else:
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


class ServoController:
    """Visual and serial interface for servo control.

    Here with the visual and serial bits stripped out - we're just using it for animations.
    """

    def __init__(self, pin, angle=90, speed=20, min_angle=45, max_angle=135):
        """Initialise the controller, with vaguely sane defaults."""
        self._servo = Servo(pin)
        self.angle = angle
        self.speed = speed

        # TODO: I don't think @property/getter/setter decorators work
        #       in Micropython, so it's a pain to do input validation.
        #       But equally, I can't find any documentation on this. Sigh.

        self.min_angle = min_angle
        self.max_angle = max_angle

        self._reversing = False

        # Set a time reference
        self._time_ref = utime.ticks_ms()

    def move(self):
        """Move the servo to the current position."""
        # self._servo.value(rescale(self.angle, 0, 180, -90, 90))
        self._servo.value(int(self.angle - 90))
        # self._servo.value(self.angle - 90)

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

        self.move()

if __name__ == '__main__':
    print ("Starting...")

    servo14 = ServoController(14, 90, 40, 45, 135)
    servo15 = ServoController(15, 90, 60, 45, 135)
    servo13 = ServoController(13, 90, 60, 45, 135)
    servo18 = ServoController(18, 90, 80, 45, 135)
    servo16 = ServoController(16, 90, 80, 45, 135)
    servo17 = ServoController(17, 90, 100, 45, 135)

    # servo12 = ServoController(12, 90, 40, 45, 135)
    # servo19 = ServoController(19, 90, 100, 45, 135)

    while True:
        servo14.update()
        servo15.update()
        servo13.update()
        servo18.update()
        servo16.update()
        servo17.update()

        # servo12.update()
        # servo19.update()
        # utime.sleep_ms(10)

