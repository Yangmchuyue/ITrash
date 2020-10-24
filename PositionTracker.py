import cv2
import numpy
#Link referenced for this code: https://pysource.com/2018/05/17/background-subtraction-opencv-3-4-with-python-3-tutorial-32/

cap = cv2.VideoCapture("hardhatVid.MOV")

#different parameters for createBackgroundSubtractorMOG2 affects how small the difference are
subtractor = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=100, detectShadows=False )

while True:
    _, frame = cap.read()
    mask = subtractor.apply(frame)
    cv2.imshow('Original', frame)
    cv2.imshow('New Image', mask)

    key = cv2.waitKey(30)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

