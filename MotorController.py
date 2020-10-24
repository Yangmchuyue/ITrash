import time
import RPi.GPIO as GPIO

MOTOR1 = 11
MOTOR2 = 12
GPIO.setup(MOTOR1, GPIO.OUT) #motor1 arduino
#GPIO.setup(XX, GPIO.OUT)
GPIO.setup(MOTOR2, GPIO.OUT) #motor2 arduino
#GPIO.setup(XX, GPIO.OUT)
US_TRIGR = 13
US_ECHO = 14
GPIO.setup(US_TRIGR, GPIO.OUT)
GPIO.setup(US_ECHO, GPIO.IN)



def ultrasonic1():
    GPIO.output(US_TRIGR, False)
    GPIO.output(US_TRIGR, True)
    time.sleep(0.00001)
    GPIO.output(US_TRIGR, False)
    pulse_start = 0
    pulse_end = 0
    while GPIO.input(US_ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(US_ECHO) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    print("distance:", distance, "cm")

while True: ########  X TO BE GIVEN BY CAMERA PI.... NEED FUNCTION TO FETCH THIS VALUE
    if ultrasonic1() > x:
        GPIO.output(MOTOR1, GPIO.HIGH)

