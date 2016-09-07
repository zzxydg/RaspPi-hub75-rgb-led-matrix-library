#!/usr/bin/env python

from rgbmatrix import RGBMatrix
from rgbmatrix import graphics
import curses
import time

PADDLE1 = 1
PADDLE2 = 2
TOP=3
BOTTOM = 4
LEFT_EDGE = 5
RIGHT_EDGE = 6

def main(win):

    # 32 Rows, 2 panel, 1 chain
    MyMatrix = RGBMatrix(32, 2, 1)

    # Bits used for PWM. Something between 1..11. Default: 11
    MyMatrix.pwmBits = 11

    # Sets brightness level. Default: 100. Range: 1..100"
    MyMatrix.brightness = 100

    # Buffer canvas.
    MyOffsetCanvas = MyMatrix.CreateFrameCanvas()

    # setup colours for border, paddles and ball
    red = graphics.Color(255, 0, 0)
    green = graphics.Color(0, 255, 0)
    blue = graphics.Color(0, 0, 255)
    white = graphics.Color(255, 255, 255)
    black = graphics.Color(0, 0, 0)
    grey = graphics.Color(128, 128, 128)

    # set player1 paddle start
    p1x = 2
    p1y = 12

    # set player2 paddle start
    p2x = 61
    p2y = 12

    # set the ball start
    ballx = 32
    bally = 16

    # Set the ball movement
    xballmovement = +1
    yballmovement = -1

    # start the main loop
    going = True

    win.nodelay(True) # make getkey() not wait

    while going:

	try:
            key = win.getkey()
	except: # in no delay mode getkey raise and exeption if no key is press
            key = None
	#endtry

	if key == "x":
	    going = False
	    break
	#endif

	# player1 paddle down
	if key == "q":
            p1y = p1y - 1
	#endif

	# player1 paddle down
	if key == "a":
            p1y = p1y + 1
	#endif

	# player2 paddle up
	if key == "p":
            p2y = p2y - 1
	#endif

	# player2 paddle down
	if key == "l":
            p2y = p2y + 1
	#endif

	ballx = ballx + xballmovement
	bally = bally + yballmovement

	p1y = bally - 4
	p2y = bally - 4

	MyMatrix.Clear()

	# draw the border
	graphics.DrawLine(MyOffsetCanvas, 0, 0, 63, 0, white)
	graphics.DrawLine(MyOffsetCanvas, 0, 0, 0 , 31, white)

	graphics.DrawLine(MyOffsetCanvas, 63, 0, 63 ,31, white)
	graphics.DrawLine(MyOffsetCanvas, 0, 31, 63, 31, white)

	# draw player1 paddle
	graphics.DrawLine(MyOffsetCanvas, p1x, p1y, p1x, p1y+8 , red)

	# draw player2 paddle
	graphics.DrawLine(MyOffsetCanvas, p2x, p2y, p2x, p2y+8 , green)

	# draw the ball
	graphics.DrawCircle(MyOffsetCanvas, ballx, bally, 1, blue)

	# Collision Detect
	collision_type = fnDetectCollision(p1x, p1y, p2x, p2y, ballx, bally)

	if collision_type == PADDLE1:
            xballmovement = +1
	#endif

	if collision_type == PADDLE2:
            xballmovement = -1
	#endif

	if collision_type == TOP:
            yballmovement = +1
	#endif

	if collision_type == BOTTOM:
            yballmovement = -1
	#endif

	if collision_type == LEFT_EDGE:
	    xballmovement = +1
	#endif

	if collision_type == RIGHT_EDGE:
	    xballmovement = -1
	#endif

	# flip on vsync
	MyOffsetCanvas = MyMatrix.SwapOnVSync(MyOffsetCanvas)

	# Wait a bit
	time.sleep(0.005)

    #endwhile

    return
#enddef

def fnDetectCollision(p1x, p1y, p2x, p2y, ballx, bally):

    # debug print
    #print("p1x=%d; p1y=%d, p2x=%d, p2y=%d, ballx=%d, bally=%d\r\n" % (p1x, p1y, p2x, p2y, ballx, bally))

    result = 0

    if ballx == p1x:
	if ((bally >= p1y) and (bally <= (p1y+8))):
	    result = PADDLE1
	#endif
    #endif

    if ballx == p2x:
	if ((bally >= p2y) and (bally <= (p2y+8))):
	    result = PADDLE2
	#endif
    #endif

    if ballx <= 0:
	result = LEFT_EDGE
    #endif

    if ballx >= 63:
	result = RIGHT_EDGE

    if bally <= 0:
	result = TOP
    #endif

    if bally >= 31:
	result = BOTTOM
    #endif

    return result
#enddef

#a wrapper to create a window, and clean up at the end
curses.wrapper(main)

#EOF
