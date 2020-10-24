import cv2

vs = cv2.VideoCapture(0)

while(True):
    # Get current frame
    ret, frame = vs.read()

    # Grayscale the image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the final image
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture 
vs.release()
cv2.destroyAllWindows()
