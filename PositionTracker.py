import cv2
import imutils
import numpy
#Link referenced for this code: https://pysource.com/2018/05/17/background-subtraction-opencv-3-4-with-python-3-tutorial-32/

cap = cv2.VideoCapture("hardhatVid.MOV")

#different parameters for createBackgroundSubtractorMOG2 affects how small the difference are
subtractor = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=1500, detectShadows=False )

while True:
    _, frame = cap.read()
    if frame is None:
        break
    frame = imutils.resize(frame, width=500)
    mask = subtractor.apply(frame)

    canny_output = cv2.Canny(mask, 100, 200)
    contours, _=cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_poly = [None] * len(contours)
    boundRect = [None] * len(contours)
    centers = [None] * len(contours)
    radius = [None] * len(contours)
    for i, c in enumerate(contours):
        contours_poly[i] = cv2.approxPolyDP(c, 3, True)
        boundRect[i] = cv2.boundingRect(contours_poly[i])
        centers[i], radius[i] = cv2.minEnclosingCircle(contours_poly[i])

    mask = numpy.zeros((canny_output.shape[0], canny_output.shape[1], 3), dtype=numpy.uint8)
    for i in range(len(contours)):
        color = (0, 0, 256)
        cv2.drawContours(mask, contours_poly, i, color)
        cv2.rectangle(mask, (int(boundRect[i][0]), int(boundRect[i][1])), \
                     (int(boundRect[i][0] + boundRect[i][2]), int(boundRect[i][1] + boundRect[i][3])), color, 2)
        cv2.circle(mask, (int(centers[i][0]), int(centers[i][1])), int(radius[i]), color, 2)

    cv2.imshow('Original', frame)
    cv2.imshow('New Image', mask)

    key = cv2.waitKey(30)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

