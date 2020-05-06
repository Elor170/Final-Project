import cv2
import requests
import Constants
import numpy as np
from Scan_board import scan_board
from Detect_board import detect_board

# video source
path = 'Resources/Lesson 6__.avi'
cap = cv2.VideoCapture(path)
# cap = cv2.VideoCapture(0)

is_first = True
is_writing = False
time_no_write = 0
is_scanned = False
frames_count = 0
success, original_frame = cap.read()

while success:
    original_frame = original_frame[0:900, :, :]
    original_frame = cv2.resize(original_frame, (1000, Constants.HEIGHT_FRAME))
    frame = original_frame
    imgWarped, coordinates = detect_board(frame)
    if imgWarped is 0:
        time_no_write = 0
        is_writing = True
        is_scanned = False
        cv2.circle(frame, (20, 20), 10, (0, 0, 255), -1)
    else:
        time_no_write += 1
        frame = imgWarped
        cv2.circle(frame, (20, 20), 10, (255, 255, 0), -1)
        if is_first:
            x = coordinates[0][0][0]
            y = coordinates[0][0][1]
            w = coordinates[3][0][0] - coordinates[0][0][0]
            h = coordinates[3][0][1] - coordinates[0][0][1]
            # print(x, y, w, h)
            # cv2.imshow("board", original_frame[y + 15: y + h - 15, x + 15: x + w - 15])
            is_first = False
            b_frame = original_frame[y + 15: y + h - 15, x + 15: x + w - 15]
            # b_frame = imgWarped[y + 5: y + h - 5, x + 5: x + w - 5]
        elif time_no_write > 5 and not is_scanned:
            is_writing = False
            a_frame = original_frame[y + 15: y + h - 15, x + 15: x + w - 15]
            # a_frame = imgWarped[y + 5: y + h - 5, x + 5: x + w - 5]
            # cv2.imshow("After", a_frame)
            # cv2.imshow("Before", b_frame)
            scan_board(b_frame, a_frame, frames_count)
            b_frame = a_frame
            is_scanned = True

    cv2.imshow("Lesson", frame)
    # cv2.imshow("O_Lesson", original_frame)
    # if is_first:
    #     cv2.waitKey(0)
    #     is_first = False
    success, original_frame = cap.read()
    if cv2.waitKey(1) & 0xFF == Constants.ESC_KEY_BOARD:
        break

cap.release()
cv2.destroyAllWindows()
