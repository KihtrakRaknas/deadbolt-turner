# Door Opener (Pico W)

This code was written in MicroPython to run on a Raspberry Pi Pico W.

The previous door opener was intended to open my college door, which required
turning the door handle in order to unlock it (it was always locked from the
outside, turning the key would turn the handle).

This new door only has a deadbolt, so this project allows you to remotely open
the door by turning the deadbolt. It is meant to work with a SG90 or MG90S
Servo motor. I 3D modeled parts to make everything work, the parts can be viewed
here: [https://a360.co/3W8fSmm](https://a360.co/3W8fSmm)

## End points

- `/turn`: Rotates servo to specified angle (with the angle query parameter), useful for finding the right angles you need
- `/open`: Rotates servo to unlock the door. Then allows the motor to freely spin.
- `/close`: Rotates servo to lock the door. Then allows the motor to freely spin.


## Set Up
Create a `config.py` folder using `config.py.template` as a reference.

The recommended way to upload MicroPython code to a Raspberry Pi Pico W is using
Thonny. You can upload the python files in this repo through the tool.