import cv2
import Const
import numpy as np
from Scan_board import scan_board
from Detect_board import detect_board


def process_video(main_window, source, output_path, scan_option, source_option):
    # video source
    cap = None
    if source_option is Const.RECORD_VIDEO:
        source_path = source
        try:
            cap = cv2.VideoCapture(source_path)
            if not cap.isOpened():
                raise NameError("The video path is invalid")
        except Exception as e:
            main_window.source_error(e)
            return

    elif source_option is Const.CAMERA:
        try:
            camera_num = int(source)
            cap = cv2.VideoCapture(camera_num)
            if not cap.isOpened():
                raise NameError("The camera number does not exist")
        except ValueError:
            main_window.source_error("The camera number is invalid")
            return
        except Exception as e:
            main_window.source_error(e)
            return

    # initialize variables
    time_no_write: int = 0
    counter: int = 1

    is_first_frame: bool = True
    is_first_scan: bool = True
    is_frame_scanned: bool = True
    is_writing: bool
    there_more_frame: bool

    processed_frame: np.ndarray
    frame_after: np.ndarray
    original_frame: np.ndarray
    frame_before = None
    board = None

    # read the first frame
    there_more_frame, original_frame = cap.read()

    while there_more_frame:
        processed_frame, is_writing = detect_board(original_frame)

        # while write - red circle
        if is_writing:
            time_no_write = 0
            is_frame_scanned = False
            cv2.circle(processed_frame, (20, 20), 10, (0, 0, 255), -1)

        # while not write - green circle
        else:
            time_no_write += 1
            cv2.circle(processed_frame, (20, 20), 10, (0, 255, 0), -1)

            # first frame
            if is_first_frame:
                is_first_frame = False
                frame_before = processed_frame

            # scan the board
            elif time_no_write > Const.FPS and not is_frame_scanned:
                frame_after = processed_frame

                if scan_option is Const.APPEND_OPTION:
                    if is_first_scan:  # create blank board
                        board = np.full((frame_before.shape[0], frame_before.shape[1], 3), 125, dtype=np.uint8)
                        is_first_scan = False

                    counter, board = scan_board(main_window, output_path, frame_before,
                                                frame_after, counter, scan_option, board)

                else:  # SEPARATE_OPTION
                    counter, _ = scan_board(main_window, output_path, frame_before, frame_after, counter, scan_option)

                frame_before = frame_after
                is_frame_scanned = True

        # show the video
        main_window.set_board_img(processed_frame.copy())

        # read the next frame
        there_more_frame, original_frame = cap.read()

        if cv2.waitKey(1) and main_window.isStopProcess:
            break

    # save the last board
    if scan_option is Const.APPEND_OPTION:
        try:
            write_check = cv2.imwrite(output_path + "/Board%d.jpg" % counter, board)
            if not write_check:
                raise NameError("The output path is invalid - output will not be saved")
        except Exception as e:
            main_window.output_error(e)

    cap.release()
    cv2.destroyAllWindows()
