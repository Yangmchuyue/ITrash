#!/usr/bin/env python3
#Reference: https://techdevops.wordpress.com/2015/03/24/non-blocking-io-keyboard-listener-in-python/
import serial
import time
import sys
import select


def pi_to_arduino():
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    while True:
        input = select.select([sys.stdin], [], [], 0.02)[0] #waits 0.02 seconds for an input
        if input:
                keyboardIn = sys.stdin.readline().rstrip()
                if(keyboardIn == "q"):
                        sys.exit(0)
                else: #input will be of form: "x z"
                        print(keyboardIn)
                        keyboardIn += "\n"
                        ser.write(keyboardIn.encode('utf-8'))
        
        
        #Reading from Arduino
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        
pi_to_arduino()
