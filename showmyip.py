#!/usr/bin/env python

import sys
import time
import netifaces as ni
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix

# get the interface name from the command line (will throw an exception if one is not given)
myifname = sys.argv[1]

# init the RGB matrix as 32 Rows, 2 panels (represents 32 x 64 panel), 1 chain
MyMatrix = RGBMatrix(32, 2, 1)

# Bits used for PWM. Something between 1..11. Default: 11
MyMatrix.pwmBits = 11

# Sets brightness level. Default: 100. Range: 1..100"
MyMatrix.brightness = 100

# Flood fill with white as a POST
MyMatrix.Fill(255, 255, 255)
time.sleep(2)
MyMatrix.Clear()

# Setup colours for text display
ColorRED = graphics.Color(255, 0, 0)
ColorGRN = graphics.Color(0, 255, 0)
ColorBLU = graphics.Color(0, 0, 255)
ColorWHI = graphics.Color(255, 255, 255)

# Create the buffer canvas
MyOffsetCanvas = MyMatrix.CreateFrameCanvas()

# Load up the font (use absolute paths so script can be invoked from /etc/rc.local correctly)
font = graphics.Font()
font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/5x8.bdf")

# get the IP address of the interface specified on the command line (e.g. wlan0)
ni.ifaddresses(myifname)
myip = ni.ifaddresses(myifname)[2][0]['addr']

# Show the interface, IP address and current time on the RGB led matrix for roughly 30 seconds (loop runs for 60 cycles with a 500ms delays, so roughly 30 seconds)
for i in range(60):
    thetime = time.strftime("%H:%M:%S")
    MyOffsetCanvas.Clear()
    graphics.DrawText(MyOffsetCanvas, font, 0, 7, ColorRED, myifname) # interface name (e.g. wlan0)
    graphics.DrawText(MyOffsetCanvas, font, 0, 15, ColorGRN, myip) # IP address
    graphics.DrawText(MyOffsetCanvas, font, 0, 23, ColorBLU, thetime) # current time (to check ntp working correctly)
    graphics.DrawText(MyOffsetCanvas, font, 0, 31, ColorWHI, str(i)) # loop counter, so we know how long before disappears
    time.sleep(0.5)
    MyOffsetCanvas = MyMatrix.SwapOnVSync(MyOffsetCanvas)
#endwhile

# tidy up and exit
MyOffsetCanvas.Clear()

#eof

