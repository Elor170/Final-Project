import cv2
import numpy as np
ESC_KEY_BOARD = 27

cap = cv2.VideoCapture('Resources/Lesson5.avi')
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
out = cv2.VideoWriter("output.avi", fourcc, 30, (640, 480), True)


while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.resize(frame, (480, 640))
    frame = frame[0:360, :]
    frame = cv2.resize(frame, (640, 480))
    out.write(frame)
    cv2.imshow("feed", frame)
    if cv2.waitKey(1) == ESC_KEY_BOARD:
        break

cv2.destroyAllWindows()
cap.release()
out.release()
