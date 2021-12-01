# PicoDisplay tinkering

The `pimoroni_` files here are all [examples from their repo](https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/examples/pico_display). Read the [product page](https://shop.pimoroni.com/products/pico-display-pack) for details on how to get started: the libraries need to be compiled into the MicroPython runtime then that flashed to the board. There's a custom Pimoroni runtime, but it may also be useful for us to know how to do this ourselves... though I _think_ the only other library we're likely to need is straight Python, which makes life simpler. Maybe.

There's also a [tutorial](https://learn.pimoroni.com/article/getting-started-with-pico).

## Actual documentation & comments

Lives here: https://github.com/pimoroni/pimoroni-pico/tree/main/libraries/pico_display

Linked from there: the [PicoGraphics library docs](https://github.com/pimoroni/pimoroni-pico/blob/main/libraries/pico_graphics/README.md#function-reference).

The library's text rendering is pretty nasty: there are several text-to-bitmap approaches out there in Python space which might be preferable, but how any of them might perform on the Pico I don't know. One issue: in my head, some of the text should be right-aligned, which is ... tricky. It might be best to pick a decent monospaced pixel font and hard-code the character glyphs ourselves. Seriously.

## Wireframe

What I want, I think, looks something like this:

```
     000----------------------180
            ^
                    v
     000----------------------180
```

The top scale represents position of servo 0, the lower is servo 1. The `^` and `v` carets move along their respective scales and back. I guess a sinusoidal animation would be nicest, but read on.

There are, conveniently, buttons in the four corners beside the numbers. So my suggestion would be: whichever button is pressed, its number changes colour and the rotary encoder affects that number.

* Interpolation towards a new target end point is interesting.
* Rotary encoder: there's a Micropython library for the ones I've ordered, [here](https://github.com/MikeTeachman/micropython-rotary) or possibly [here](https://github.com/mdxtinkernick/pico_encoders)

At some point, we would probably want to use the rotary encoder button to control things like:

* Animation type: linear or sinusoidal
* Animation rate: even slow/medium/fast would likely be helpful.
* A mode where you just dial in a position and the servo stays there: so, direct control as you twiddle the encoder.
* A mode where we somehow control neopixels, if and when we integrate them into all of this (coloured eyes might be nice to include, for exmaple). So, a hue scale or something like that.
