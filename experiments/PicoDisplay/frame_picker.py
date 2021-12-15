## Test code to work out how to create the programmable animation that doesn't interupt and timing.
import utime

## First we need start and end points of the cycle
## These are between 0, and 180 degrees.

x_start = 0
x_end = 180   # note that this isn't the end of the cycle, actually the middle.
x_current = 0

## The total length of the line in pixels is from x pixel 50 to x pixel 140
x_pixel_start = 50
x_pixel_end = 140
max_line_length = 90

## We need to define a frame rate, I'm guessing 24fps, and a cycle duration 1 second.
frame_rate = 24
cycle_duration = 1
frames_per_cycle = frame_rate * cycle_duration

time_now = utime.ticks_ms()
time_prev = time_now

frame_counter = 0

top_x_position = []


## I need an array that stores the x positions for each frame
for i in range(frames_per_cycle/2):
    # take the current frame number and calc the angular position
    x_current = int(x_start + (i/frames_per_cycle)*(x_end - x_start)
    
    # take the angular position and then find the x pixel location
    


while True:
    time_now = utime.ticks_ms()
    if (time_now - time_prev) > 5000:
        ## Advnce the frame
        print("Ping")
        if frame_counter == frames_per_cycle:
            frame_counter = 0
        



        print(time_now - time_prev)
        time_prev = time_now