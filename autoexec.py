#!/usr/bin/env python

import time
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix

# init the RGB matrix as 32 Rows, 2 panels (represents 32 x 64 panel), 1 chain
MyMatrix = RGBMatrix(32, 2, 1)

# Bits used for PWM. Something between 1..11. Default: 11
MyMatrix.pwmBits = 11

# Sets brightness level. Default: 100. Range: 1..100"
MyMatrix.brightness = 100

# set colour
ColorWHI = graphics.Color(255, 255, 255)

# Create the buffer canvas
MyOffsetCanvas = MyMatrix.CreateFrameCanvas()

# Load up the font (use absolute paths so script can be invoked from /etc/rc.local correctly)
font = graphics.Font()
font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/5x8.bdf")

graphics.DrawText(MyOffsetCanvas, font, 0, 7, ColorWHI, "invoked:")
graphics.DrawText(MyOffsetCanvas, font, 0, 15, ColorWHI, "autoexec.py")
MyOffsetCanvas = MyMatrix.SwapOnVSync(MyOffsetCanvas)
time.sleep(1.0)
MyOffsetCanvas.Clear()

