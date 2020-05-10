import cv2
import Constants
from Scan_board import scan_board
from Detect_board import detect_board

# video source
path = 'Resources/Lesson_1.mp4'
cap = cv2.VideoCapture(path)

case = Constants.SEPARATE_CASE
is_first = True
is_writing = True
is_scanned = True
time_no_write = 0
counter = 1
success, original_frame = cap.read()

while success:
    original_frame = cv2.resize(original_frame, (Constants.HEIGHT_FRAME, Constants.WIDTH_FRAME))
    processed_frame, is_writing = detect_board(original_frame)
    # while write
    if is_writing:
        time_no_write = 0
        is_scanned = False
        cv2.circle(processed_frame, (20, 20), 10, (0, 0, 255), -1)
    # while not write
    else:
        time_no_write += 1
        cv2.circle(processed_frame, (20, 20), 10, (255, 255, 0), -1)
        # first frame
        if is_first:
            is_first = False
            before_frame = processed_frame
        # scan the board
        elif time_no_write > 60 and not is_scanned:
            after_frame = processed_frame
            counter, board = scan_board(before_frame, after_frame, counter, case)
            before_frame = after_frame
            is_scanned = True
    cv2.imshow("Lesson", processed_frame)
    success, original_frame = cap.read()
    if cv2.waitKey(1) & 0xFF == Constants.ESC_KEY_BOARD:
        break

if case is Constants.APPEND_CASE:
    cv2.imwrite("Output/Board.jpg", board)

cap.release()
cv2.destroyAllWindows()
