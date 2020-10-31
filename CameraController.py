import cv2
import TargetTrajectoryTracker
import imutils
import numpy
import time
 
def getNextFrame(centerOne):
    print("Sleep Start")
    time.sleep(0.25)
    print("Sleep End")
    
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
    
    #============================================================
    # Source: https://www.pyimagesearch.com/2015/09/21/opencv-track-object-movement/
    # Using the mask found from the previous step, we use the
    # algorithm below to find and circle the contours.
    #============================================================

   
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    centerTwo = None
   
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        if M["m00"]!=0:
            centerTwo = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # only proceed if the radius meets a minimum size
        if radius > 10:
            #draw the circle and centroid on the frame,
            #then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            # cv2.circle(frame, centerTwo, 5, (0, 0, 255), -1)
    #============================================================
    if centerTwo==None:
        return
    print("test3")

    print(centerOne)
    print(centerTwo)
    print("test4")

    coord = TargetTrajectoryTracker.predictCoord((centerOne[0], centerOne[1], 0), (centerTwo[0], centerTwo[1], 0), 0.25)
    
    print("test5")
    print(int(coord[0]),int(coord[1]))
    # cv2.circle(frame, (int(coord[0]), 500-int(coord[1])), 5, (0, 255, 0), -1)
    cv2.circle(frame, (int(coord[0]), 500-10), 5, (0, 255, 0), -1)
    cv2.imshow("FrameTrajectoryPredict", frame)
    print("test6")
    time.sleep(2)

       
# Intialize Video Capture
vs = cv2.VideoCapture(0)
#vs = cv2.VideoCapture("hardhatVid.MOV")

subtractor = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=100, detectShadows=False )
ret, frame = vs.read()

while(True):
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
    
    #============================================================
    # Source: https://www.pyimagesearch.com/2015/09/21/opencv-track-object-movement/
    # Using the mask found from the previous step, we use the
    # algorithm below to find and circle the contours.
    #============================================================

    
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None
    
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        if M["m00"]!=0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            print("hello")
            getNextFrame(center)
    #============================================================
    
    
    
    # Display the final image
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
vs.release()
cv2.destroyAllWindows()



    

