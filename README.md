# Connect Trainer

Exercise those servos!

Intended as a helper tool for Connect workshops, assuming direct control over Kniwwelino-connected servos from a handy little widget. The widget commands servo sweeps between end points which may be dialled in using a rotary encoder, offering a read-out of servo angle to assist in calibrations.

Lots of ways of doing this, potentially. So far (2021-09-30):

- Serial would be easy enough, but then we're doing multiple things through the USB port. Like... programming the boards.
- We'd originally assumed the Trainer would be a full-fat Pi in a box with a bunch of buttons and dials and a screen. We even talked about a printer to output servo endpoints. But the bill of materials for that would be quite high, and on reflection I think workshops would benefit from having one Trainer per desk, rather than one per workshop.
- A cheaper option would be to use a Pico as the Trainer, with a Pimoroni Pico Display for output. Neat.
- ...but it turns out ESP8266 modules can't do I2C peripheral mode, and the Pico Micropython I2C module doesn't yet have an I2C responder. Both ends want to be controller.
- Next thing to try: SoftwareSerial.

