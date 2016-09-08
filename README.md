# RaspPi-hub75-rgb-led-matrix-library

RGB LED Matrix code built around the library created by Henner Zeller

The library can be found on GitHub here: https://github.com/hzeller/rpi-rgb-led-matrix

The code in this repository is very much work in progress with little documentation at the moment.

A video of the module construction, standard demo and my pong can be found on YouTube here: https://youtu.be/10MrYqf3euI

A Footnote on the purpose of bootstrap.py and autoexec.py:

The RaspberryPi being used to power the RGB matrix in my setup is running headless with a USB wifi adapter.  Pre-loaded onto the SD card are a number of programs written in python that use the RGB matrix for output (e.g. pong.py)
In my setup I remote into the RaspberryPi to invoke the programs.
My network is setup to use DHCP and when the RaspberryPi boots there is potential for it to be assigned a new IP address by the router, so the problem of how to find out the new address without using nmap or logging into the router exists.
The solution: Get the RaspberryPi to print out its' IP address on boot to the RGB matrix to allow SSH connections for control ... simple.

As an improvement, so that I can choose which program is invoked automatically (if needed) following bootup I have modified bootstrap.py to call autoexec.py (sorry, DOS background) once it has finished, as a new process with root permissions.  The example shown for autoexec.py is just a stub that proves the mechanism works, but this file could be replaced with any python program.

Simple and effective.

Enjoy!
