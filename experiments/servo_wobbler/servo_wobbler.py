from time import sleep
from servo import Servo

s1 = Servo(14)

def sweep_up(servo):
    for angle in range(-90, 90, 1):
        servo.value(angle)
        sleep(0.01)

def sweep_down(servo):
    for angle in range(90, -90, -1):
        servo.value(angle)
        sleep(0.01)

def sweep_up_and_down(servo):
    sweep_up(servo)
    sweep_down(servo)

for _ in range(3): # '_' is a placeholder variable: we don't need it in the loop
    sweep_up_and_down(s1)

s1.disable()
