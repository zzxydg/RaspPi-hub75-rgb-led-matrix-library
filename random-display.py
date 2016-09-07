#!/usr/bin/env python

from random import randint
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix
import numpy

def main():
    # init the RGB matrix as 32 Rows, 2 panels (represents 32 x 64 panel), 1 chain
    MyMatrix = RGBMatrix(32, 2, 1)

    # Bits used for PWM. Something between 1..11. Default: 11
    MyMatrix.pwmBits = 11

    # Sets brightness level. Default: 100. Range: 1..100"
    MyMatrix.brightness = 25

    # Create the buffer canvas
    MyOffsetCanvas = MyMatrix.CreateFrameCanvas()
    
    # clear down the matrix
    MyOffsetCanvas.Clear()

    # loops of random colour pixels
    for z in range(0, 256):
        for x in range(0,64):
            for y in range(0,32):
                R = numpy.random.randint(0, 255)
                G = numpy.random.randint(0, 255)
                B = numpy.random.randint(0, 255)
                MyOffsetCanvas.SetPixel(x, y, R, G, B)
            #endfor
        #endfor
        MyOffsetCanvas = MyMatrix.SwapOnVSync(MyOffsetCanvas)
    #endfor

    return
#endef

if __name__ == '__main__':
    main()
#endif    
