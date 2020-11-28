#!/usr/bin/env python3
# Reference: https://techdevops.wordpress.com/2015/03/24/non-blocking-io-keyboard-listener-in-python/
import serial
import time
import sys
import select


def arduinoToPi():
    # a = 0   # leave here for use in MainPi.py
    line = ser.readline().decode('utf-8').rstrip()
    if line != " " and line != "" and line != "\n":
        print(line)


def piToArduino():
    input = select.select([sys.stdin], [], [], 0.02)[
        0]  # waits 0.02 seconds for an input
    if input:
        # input will be "x z", "q" (quit), or " " (pause/unpause)
        keyboardIn = sys.stdin.readline().rstrip()
        print(keyboardIn)
        keyboardIn += "\n"
        ser.write(keyboardIn.encode('utf-8'))
        if (keyboardIn == "q"):  # turn off the robot and the log
            sys.exit(0)


ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()
##
time.sleep(3)
while True:
    piToArduino()
    arduinoToPi()
