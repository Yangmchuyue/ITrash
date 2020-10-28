import time
import RPi.GPIO as GPIO

# set up
motorX = 11
motorZ = 12
directionX = 21 #forward and backwards
directionZ = 22
GPIO.setup(motorX, GPIO.OUT) #motor1 arduino
GPIO.setup(motorZ, GPIO.OUT) #motor2 arduino
GPIO.setup(directionX, GPIO.OUT) #motor1 arduino
GPIO.setup(directionZ, GPIO.OUT) #motor2 arduino

trigrR = 13
echoR = 14
GPIO.setup(trigrR, GPIO.OUT)
GPIO.setup(echoR, GPIO.IN)

trigrB = 13
echoB = 14
GPIO.setup(trigrB, GPIO.OUT)
GPIO.setup(echoB, GPIO.IN)

# functions
def ultrasonic():
    global distanceR, distanceB
# right
    pulse_start = 0
    pulse_end = 0
    GPIO.output(trigrR, False)
    GPIO.output(trigrR, True)
    time.sleep(0.00001)
    GPIO.output(trigrR, False)
    while GPIO.input(echoR) == 0:
        pulse_start = time.time()
    while GPIO.input(echoR) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distanceR = round(pulse_duration * 17150, 2)
# bottom
    pulse_start = 0
    pulse_end = 0
    GPIO.output(trigrB, False)
    GPIO.output(trigrB, True)
    time.sleep(0.00001)
    GPIO.output(trigrR, False)
    while GPIO.input(echoB) == 0:
        pulse_start = time.time()
    while GPIO.input(echoB) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distanceB = round(pulse_duration * 17150, 2)

    print("distance:", distanceR, "cm")
    print("distance:", distanceB, "cm")

while True: #NOTE:  X and Z TO BE GIVEN BY CAMERA PI.... NEED FUNCTION TO FETCH THIS VALUE
    ultrasonic()
    x = 0
    z = 0
    if distanceR > x:
        GPIO.output(directionX, GPIO.HIGH)
        GPIO.output(motorX, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(motorX, GPIO.LOW)

    if distanceR < x:
        GPIO.output(directionX, GPIO.LOW)
        GPIO.output(motorX, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(motorX, GPIO.LOW)

    if distanceB > z:
        GPIO.output(directionZ, GPIO.HIGH)
        GPIO.output(motorZ, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(motorZ, GPIO.LOW)

    if distanceB < z:
        GPIO.output(directionZ, GPIO.LOW)
        GPIO.output(motorZ, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(motorZ, GPIO.LOW)

    if abs(distanceR - x) < 1 and abs(distanceB - z):
        GPIO.output(motorX, GPIO.LOW)
        GPIO.output(motorZ, GPIO.LOW)
        break

