from machine import UART, Pin
import picodisplay as display
import utime

buf = bytearray(display.get_width() + display.get_height() *2)
display.init(buf)
display.setbacklight(0.8)

class WaitScreen:
    """Display a wait screen with animation ticker."""

    def __init__(self, wait_cycle_time=2000, circle_rad_min=6, circle_rad_max=20, in_circle_min=4, in_circle_max=18):
        """Initialise the controller, with sane defaults."""
        self.wait_cycle_time = wait_cycle_time
        self.circle_rad_min = circle_rad_min
        self.circle_rad_max = circle_rad_max
        self.in_circle_min = in_circle_min
        self.in_circle_max = in_circle_max
        self._radius = self.in_circle_min
        self._rising = True

        self._start_time = utime.ticks_ms()

        def draw(self):
            _now_time = utime.ticks_ms()
            _elapsed_time = _now_time - self._start_time
            if self._rising:
                # Calculate radius between in_circle_min and circle_rad_max, in wait_cycle_time
                self._radius = self.in_circle_min + ( (self.in_circle_max - self.in_circle_min) / (self._start_time + self._wait_cycle_time) * )





