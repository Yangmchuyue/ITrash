import cv2
import TargetTrajectoryTracker

# Intialize Video Capture
vs = cv2.VideoCapture(0)
#vs = cv2.VideoCapture("hardhatVid.MOV")

subtractor = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=100, detectShadows=False )

while(True):
    # Get current frame
    ret, frame = vs.read()

    # Grayscale the image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Resize the image
    resize = cv2.resize(gray, (500, 500))
    
    # Apply mask onto the image
    mask = subtractor.apply(resize)
    
    # Display the final image
    cv2.imshow('Mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
vs.release()
cv2.destroyAllWindows()
