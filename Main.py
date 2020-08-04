import cv2
import Const
import numpy as np
from Scan_board import scan_board
from Detect_board import detect_board


# video source
path: str = 'Resources/Lesson_2.mp4'
cap: cv2.VideoCapture = cv2.VideoCapture(path)

scan_option: int = Const.APPEND_OPTION

# initialize variables
time_no_write: int = 0
counter: int = 1
is_first: bool = True
is_first_scan: bool = True
is_writing: bool = True
is_scanned: bool = True

processed_frame = None
before_frame = None
after_frame = None
board = None

there_more_frame: bool
original_frame: np.ndarray
there_more_frame, original_frame = cap.read()

while there_more_frame:
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
            counter, board = scan_board(before_frame, after_frame, counter, scan_option, board)
            before_frame = after_frame
            is_scanned = True
    h = processed_frame.shape[0]//2
    w = processed_frame.shape[1]//2
    cv2.imshow("Lesson", cv2.resize(processed_frame, (w, h)))
    there_more_frame, original_frame = cap.read()
    if cv2.waitKey(1) & 0xFF == Const.ESC_KEY_BOARD:
        break

if scan_option is Const.APPEND_OPTION:
    cv2.imwrite("Output/Board%d.jpg" % counter, board)

cap.release()
cv2.destroyAllWindows()
