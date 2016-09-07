#!/usr/bin/env python

import sys
import time
import netifaces as ni
import subprocess

from rgbmatrix import graphics
from rgbmatrix import RGBMatrix

def str_left(s, amount):
    return s[:amount]
#enddef

def str_right(s, amount):
    return s[-amount:]
#enddev

def str_mid(s, offset, amount):
    return s[offset:offset+amount]
#enddef

def main(myifname):

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
        # grab current time and format
        thetime = time.strftime("%H:%M:%S")

        # run the "iwconfig" command passing in the ifname and capturing the output
        cmd = subprocess.Popen('iwconfig %s' % myifname, shell=True, stdout=subprocess.PIPE)

        # example output from "iwconfig wlp2s0" from Asus Eee PC R101 running lubuntu 16.04
        #
        # wlp2s0    IEEE 802.11bg  ESSID:"wapifoh"  
        # Mode:Managed  Frequency:2.437 GHz  Access Point: E8:FC:AF:2B:09:60   
        # Bit Rate=54 Mb/s   Tx-Power=20 dBm   
        # Retry short limit:7   RTS thr:off   Fragment thr:off
        # Power Management:off
        # Link Quality=30/70  Signal level=-80 dBm  
        # Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
        # Tx excessive retries:0  Invalid misc:2280   Missed beacon:0
        #

        # scan the output looking for key tokens of "Link Quality" "Level" and "ESSID"
        for line in cmd.stdout:
            if 'Link Quality' in line:
                pos = line.find('Quality=')
                quality = str_mid(line, pos+8, 5)

                pos = line.find('level=')
                level = str_mid(line, pos+6, 7)
            #endif
            
            if 'ESSID' in line:
                pos = line.find('ESSID:')
                essid = str_mid(line, pos+7, len(line)-pos-11)
            #endif
        #endfor

        # format the interface attributes into four lines
        line1 = str("%s %s" % (myifname, essid))
        line2 = str("%s %s" % (quality, level))
        line3 = str("%s" % myip)
        line4 = str("%s %s" % (thetime, str(i)))

        # clear matrix and print the four lines        
        MyOffsetCanvas.Clear()
        graphics.DrawText(MyOffsetCanvas, font, 0,  7, ColorRED, line1)
        graphics.DrawText(MyOffsetCanvas, font, 0, 15, ColorGRN, line2)
        graphics.DrawText(MyOffsetCanvas, font, 0, 23, ColorBLU, line3)
        graphics.DrawText(MyOffsetCanvas, font, 0, 31, ColorWHI, line4)

        # debug print
        print("line1=%s; line2=%s; line3=%s; line4=%s" % (line1,line2,line3,line4))
        
        time.sleep(0.5)
    
        MyOffsetCanvas = MyMatrix.SwapOnVSync(MyOffsetCanvas)
    #endwhile

    # tidy up and exit
    MyOffsetCanvas.Clear()

    # invoking autoexec.py	
    graphics.DrawText(MyOffsetCanvas, font, 0, 7, ColorWHI, "invoking:")
    graphics.DrawText(MyOffsetCanvas, font, 0, 15, ColorWHI, "autoexec.py")
    MyOffsetCanvas = MyMatrix.SwapOnVSync(MyOffsetCanvas)
    time.sleep(1.0)

    # invoke the autoeec.py python project in /projects with root permissions
    # Other python projects to run should replace autoexec.py with there own functionality
    # invoking with root allows these projects to do anything!
    cmd = subprocess.Popen('sudo python /home/pi/projects/autoexec.py', shell=True, stdout=subprocess.PIPE)

#enddef

# entry point
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("You must specify the ifname!")
        exit(1)
    else:
        # get the interface name from the command line and pass in
        main(sys.argv[1])
    #endif
#endif
