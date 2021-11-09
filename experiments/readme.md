# Experiments directory

This is what I've tried as of 2021-11-09 to get a Pico and an ESP8266 to talk to each other. Or at least, an 8266 to listen to a Pico. So far, I haven't been successful.

The basic setup is:

Thonny
    \--> USB UART
               \--> Pico
                      \--> UART pins
                                \--> SoftwareSerial on ESP8266
                                                            \--> USB Serial
                                                                    \--> Arduino IDE

Pico pins 4 and 5 are wired to Wemos D1 pins D1 and D2 (I'm not clear what the correct way around here would be). Grounds are also connected. At the moment, I don't seem to have the combination of pins and serial connection invocations correct, and I'm not seeing messages passed between the two boards.

Test code in `/Experiments` consists of PicoSerial (Pico) and `softwareSerialParse.ino` (ESP8266).

## PicoSerial

Micropython script to fire a few things at one of the Pico's UARTs (pins 4 and 5), in a loop. Best run from within Thonny, on the Pico, so you can see the output (which is just `print()` - there's no message return path in use at present).

Note that in this circumstance, you'll have both UARTs in use: the one being used by the script, and one over USB for Thonny.

## softwareSerialParse

Proof-of-concept as one end of the Pico-to-ESP8266 serial connection. Uses [SoftwareSerial library](https://www.arduino.cc/en/Reference/softwareSerial) on pins D1 and D2. Also uses USB as a standard serial connection, to output diagnostics.

The ESP has one UART, but SoftwareSerial should be able to handle another channel for us. Note that the SoftwareSerial implementation on ESP should probably be [espsoftwareserial](https://github.com/plerup/espsoftwareserial). From my reading of that readme, this is the version that will be pulled in by Arduino IDE on an ESP board anyway.

## serialecho

Most-basic-possible ESP8266 Serial script. Just echoes whatever comes in. Which, since that's coming in over USB, isn't terribly useful. Use the serial monitor in Arduino IDE.

## serialParse

Checking I understand serial string semantics correctly. Just like `serialecho`, but if the line received reads 'cabbage,' the script returns `cabbage...is horrid`, and a counter.

