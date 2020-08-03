import cv2
import Const
from Scan_board import scan_board
from Detect_board import detect_board
import numpy as np

# video source
path = 'Resources/Lesson_2.mp4'
cap = cv2.VideoCapture(path)

case = Const.APPEND_CASE
is_first = True
is_first_scan = True
is_writing = True
is_scanned = True
time_no_write = 0
counter = 1
processed_frame = None
before_frame = None
after_frame = None
board = None
success, original_frame = cap.read()

while success:
    processed_frame, is_writing = detect_board(original_frame)
    # while write
    if is_writing:
        time_no_write = 0
        is_scanned = False
        cv2.circle(processed_frame, (20, 20), 10, (0, 0, 255), -1)

    # while not write
    else:
        time_no_write += 1
        cv2.circle(processed_frame, (20, 20), 10, (0, 255, 0), -1)
        # first frame
        if is_first:
            is_first = False
            before_frame = processed_frame
        # scan the board
        elif time_no_write > Const.FPS and not is_scanned:
            after_frame = processed_frame
            if is_first_scan:
                board = np.full((before_frame.shape[0], before_frame.shape[1], 3), 125, dtype=np.uint8)
                is_first_scan = False
            counter, board = scan_board(before_frame, after_frame, counter, case, board)
            before_frame = after_frame
            is_scanned = True
    h = processed_frame.shape[0]//2
    w = processed_frame.shape[1]//2
    cv2.imshow("Lesson", cv2.resize(processed_frame, (w, h)))
    success, original_frame = cap.read()
    if cv2.waitKey(1) & 0xFF == Const.ESC_KEY_BOARD:
        break

if case is Const.APPEND_CASE:
    cv2.imwrite("Output/Board%d.jpg" % counter, board)

cap.release()
cv2.destroyAllWindows()
