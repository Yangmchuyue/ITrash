import cv2
import numpy

img1 = cv2.imread('background_image.jpg', cv2.IMREAD_UNCHANGED)
first_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
first_gray = cv2.GaussianBlur(first_gray, (5, 5), 0)
img2 = cv2.imread('hardhat_photo1.jpg', cv2.IMREAD_UNCHANGED)
finalImg = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
finalImg = cv2.GaussianBlur(finalImg, (5, 5), 0)

difference = cv2.absdiff(first_gray, finalImg)

cv2.imshow('Background', first_gray)
cv2.imshow('Original', finalImg)
cv2.imshow('Difference', difference)
cv2.waitKey(0)

