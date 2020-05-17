import cv2
import requests
import Constants
import numpy as np
from Scan_board import scan_board
from Detect_board import detect_board

# video source
url = 'http://192.168.137.125:8080//shot.jpg'

is_first = True
is_writing = False
is_scanned = False
time_no_write = 0
old_coordinates = 0

while True:
    frame_resp = requests.get(url)
    frame_arr = np.array(bytearray(frame_resp.content), dtype=np.uint8)
    original_frame = cv2.imdecode(frame_arr, -1)
    original_frame = cv2.resize(original_frame, (Constants.HEIGHT_FRAME, Constants.WIDTH_FRAME))
    processed_frame, is_writing, new_coordinates = detect_board(original_frame, old_coordinates)
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
            old_coordinates = new_coordinates
            before_frame = processed_frame
        # scan the board
        elif time_no_write > 25 and not is_scanned:
            after_frame = processed_frame
            scan_board(before_frame, after_frame)
            before_frame = after_frame
            is_scanned = True

    cv2.imshow("Lesson", processed_frame)
    if cv2.waitKey(1) & 0xFF == Constants.ESC_KEY_BOARD:
        break

cv2.destroyAllWindows()
