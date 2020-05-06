import argparse
import cv2

# load the video
cap = cv2.VideoCapture('Lesson5.avi')
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# load and show the first frame
ret, frame1 = cap.read()
frame1 = cv2.resize(frame1, (480, 640))


# close all open windows
cv2.destroyAllWindows()
cap.release()



