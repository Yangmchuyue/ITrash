#!/usr/bin/env python3
import serial
import time

x = 5
z = 3

def pi_to_arduino(x,z):
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    while True:
        x = input('x=')
        z = input('z=')
        x1 = str(x).encode('utf-8')
        z1 = str(z).encode('utf-8')
        ser.write(x1)
        ser.write(b"\n")
        ser.write(z1)
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)

           
pi_to_arduino(x,z)
