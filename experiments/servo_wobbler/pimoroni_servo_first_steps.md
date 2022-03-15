# Getting started with Servos on a Pi Pico

## What's a 'servo'?

[image]

This is a microservo. Inside the blue case is a small electric motor, geared to move the white plastic part on top, which is called a 'servo horn'. Most servos can rotate over a 180 degree range. They're commonly used to move parts of models or devices, by instructing them to move to a specific angle within that range.

Servos can be finicky devices. Their control mechanism is peculiar, and there can be a lot of variation from one brand or type of servo to another. So there's a lot of complexity for a servo software library to handle.

One particular issue is that servos are commonly designed to run at 5 Volts, when most electronic devices now run at 3.3 Volts. Some servos handle this better than others. If you're starting out, it's helpful to use servos which work at least fairly reliably when under-volted.

While purely digital servos exist, common types are usually controlled via Pulse-Width Modulation (PWM). The servo angle follows the width of a control pulse signal sent continuously, with a specific signal frequency. The implications of this are:

* Controlling servos requires precise timings from the controller board.
* Often, servos will 'hunt' or jitter. This can be charming or characterful if you're making puppets, or irritating if you're building robots.
* Servo libraries have to work around myriad issues; some are more succesful than others.
* A really good servo library hides all of this from you, until you need it. But please remember: if you find servo control easy, that's because somebody else sweated for hours to make it easy.

### Suppliers of suitable servos

#### UK

The most reliable source of 3.3V-capable microservos we've found is Kitronik. Specifically [this item](https://kitronik.co.uk/collections/robotics/products/2565-180-mini-servo), which works at well with Arduino, Micro:Bit, Raspberry Pi, and Pi Pico.

## First steps - making a servo move

This guide assumes the specific example of the Kitonik-sourced servo noted above, and a Raspberry Pi Pico controller.

### Install Pimoroni MicroPython

The Servo library is compiled into the Pimoroni MicroPython distribution.

> Instruction here, presumably from existing Pimoroni docs.

### Wiring

Servos need power (+3.3V and ground), and a control signal

TODO: Fritzing diagram here.

### Example 1: first movement

Assumptions:

* You're comfortable running Python code on the Pico, using something like the Thonny editor. If not, [this book](https://hackspace.raspberrypi.com/books/micropython-pico) is a good place to start. There's a 'free download' button at that link, or you can buy a copy if that's your preference.

```python
from time import sleep
from servo import Servo

s1 = Servo(14)  # Creates a Servo object on pin 14.

s1.enable()     # Servo receives power and con
s1.to_max()     # Move to maximum angle (+90 degrees)
sleep(1)        # Pause 1 second
s1.to_mid()     # Move to midpoint (0 degrees)
sleep(1)
s1.to_min()     # Move to minimum angle (-90 degrees)
sleep(1)
```

Paste the above into Thonny (or your preferred editor), run it, and the servo should move to its maximum, middle and minimum positions, with short pauses in between.

### Example 2: Angle control

While the `to_min()`, `to_mid()` and `to_max()` calls are occasionally handy, it's more typical to want precise control over a servo. Here's an example:

```python
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
```

Run this, and it'll sweep the servo back and forth three times. Things to note:

* The `enable()` call isn't necessary here - the .`value()` method will do that for you.
* As the servo moves, you might notice that it doesn't _quite_ rotate through 180 degrees. Welcome to the slightly vague world of servos, where the physical device treats your strict program command more like a suggestion.
* The `disable()` call at the end turns the servo off. This stops it buzzing, but also stops it from working to maintain its position. In some cases, that's not what you want: the thing the servo's connected to might sag. With `enable()` and `disable()` you can choose whether to accept the buzz or the sag.

### Example 3: changing ranges

In many situations it makes sense for the servo to move between -90 and +90 degrees, with the centre point at 0. But if you've come from an Arduino Servo world, you might be more used to a range between 0 and 180. The Servo library can help you here, via a calibration.

```python
s1cal = s1.calibration()
s1cal.point_at(0)




