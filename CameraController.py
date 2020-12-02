import cv2
import TargetTrajectoryTracker
import imutils
import numpy
import time
import socket
import sys
import select
import os

# Windows
if os.name == 'nt':
    import msvcrt

# duplicate for each client

host = '192.168.1.79'  # update after setup
port = int(input("Port: "))

def setupSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s


def transmit(message):
    try:
        s = setupSocket()
        s.send(str.encode(message))
        s.close
    except:
        print("Connection Error")


def detectObject(mask):
    # ============================================================
    # Source: https://www.pyimagesearch.com/2015/09/21/opencv-track-object-movement/
    # Using the mask found from the previous step, we use the
    # algorithm below to find and circle the contours.
    # ============================================================

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    centre = None

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        if radius > 2 and radius < 60:
            if M["m00"] != 0:
                centre = (int(M["m10"] / M["m00"]),
                          int(M["m01"] / M["m00"]))
    # ============================================================
    return centre


def convertPixeltoMetre(point):
    xScale = 1.80
    yScale = 1.70

    return (point[0]/500 * xScale, point[1]/500 * yScale)


def convertMetretoPixel(point):
    xScale = 1.80
    yScale = 1.70

    return (int(point[0]/xScale * 500), int(point[1]/yScale * 500))


# Intialize Video Capture
vs = cv2.VideoCapture(2)
# vs = cv2.VideoCapture("Test_video.MOV")

# Intialize Background Subtractor
subtractor = cv2.createBackgroundSubtractorMOG2(
    history=100, varThreshold=100, detectShadows=False)


out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(
    'M', 'J', 'P', 'G'), 10, (500, 500))

for x in range(30):
    ret, frame = vs.read()

pause = False
red = (0, 0, 255)
green = (0, 255, 0)
blue = (255, 0, 0)

time.sleep(1)

while(True):
    # Check for keyboard input to pause/unpause
    '''
    input = select.select([sys.stdin], [], [], 0.02)[0]
    if input:
        keyboardIn = sys.stdin.readline().rstrip()
        if keyboardIn == "":
            if pause:
                pause = False
            else:
                pause = True
    '''
    #if msvcrt.getch() == '\n' and pause:
    if pause:
        if input():
            print("Unpause")
            pause = False

    # Get current frame
    ret, frame = vs.read()

    # Resize the image
    frame = cv2.resize(frame, (500, 500))

    # Grayscale the image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Resize the image
    resize = cv2.resize(gray, (500, 500))

    # Apply mask onto the image
    mask = subtractor.apply(resize)

    centreOne = detectObject(mask)

    if centreOne != None:
        time.sleep(0.25)

        # Get current frame
        ret, frame = vs.read()

        # Resize the image
        frame = cv2.resize(frame, (500, 500))

        # Grayscale the image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Resize the image
        resize = cv2.resize(gray, (500, 500))

        # Apply mask onto the image
        mask = subtractor.apply(resize)

        centreTwo = detectObject(mask)

        if centreTwo != None:
            centreOne = convertPixeltoMetre((centreOne[0], 500-centreOne[1]))
            centreTwo = convertPixeltoMetre((centreTwo[0], 500-centreTwo[1]))

            coord = TargetTrajectoryTracker.predictCoord(
                (centreOne[0], centreOne[1]), (centreTwo[0], centreTwo[1]), 0.1)

            #Threshold for how far the robot can move away from wall.
            if coord[0] > 1.00:
                coord[0] = 1.00

            if not pause:
                mesg = "x " + str(int(100*coord[0]))
                transmit(mesg)
                pause = True

            centreOne = convertMetretoPixel(centreOne)
            centreTwo = convertMetretoPixel(centreTwo)
            coord = convertMetretoPixel(coord)

            pos1 = "(" + str(centreOne[0]) + ", " + str(centreOne[1]) + ")"
            pos2 = "(" + str(centreTwo[0]) + ", " + str(centreTwo[1]) + ")"
            pos3 = "(" + str(int(coord[0])) + ", " + str(int(coord[1])) + ")"

            cv2.putText(frame, pos1, (centreOne[0], 500-centreOne[1]),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, red, 2, cv2.LINE_AA)
            cv2.putText(frame, pos2, (centreTwo[0], 500-centreTwo[1]),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, green, 2, cv2.LINE_AA)
            cv2.putText(frame, pos3, (int(coord[0]), (500-int(coord[1]))),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, blue, 2, cv2.LINE_AA)

            cv2.circle(frame, (centreOne[0], 500-centreOne[1]), 5, red, -1)     # red
            cv2.circle(frame, (centreTwo[0], 500 - centreTwo[1]), 5, green, -1) # green
            cv2.circle(frame, (int(coord[0]), 500-int(coord[1])), 5, blue, -1)  # blue


    out.write(frame)

    # Display the final image
    frame = cv2.resize(frame, (850, 850))
    cv2.imshow("Frame3", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
vs.release()
cv2.destroyAllWindows()
