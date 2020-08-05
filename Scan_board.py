import cv2
import Const
import numpy as np
import imutils
from skimage.metrics import structural_similarity


def create_new_board(option, is_new_board_added, counter, board):
    if option is Const.APPEND_OPTION and not is_new_board_added:
        is_new_board_added = True
        cv2.imwrite("Output/Board%d.jpg" % counter, board)
        board = np.full((board.shape[0], board.shape[1], 3), 125, dtype=np.uint8)
        counter += 1
    return is_new_board_added, counter, board


# b_img = the image before, a_img = the image after 
def scan_board(b_img, a_img, counter, option, board=None):
    # preprocessing
    is_something_written: bool = False
    is_new_board_added: bool = False

    a_img = cv2.resize(a_img, (b_img.shape[1], b_img.shape[0]))
    a_img_copy: np.ndarray = a_img.copy()
    b_img_copy: np.ndarray = b_img.copy()

    b_gray: np.ndarray = cv2.cvtColor(b_img, cv2.COLOR_RGB2GRAY)
    a_gray: np.ndarray = cv2.cvtColor(a_img, cv2.COLOR_RGB2GRAY)
    b_gray = cv2.GaussianBlur(b_gray, (5, 5), 1)
    a_gray = cv2.GaussianBlur(a_gray, (5, 5), 1)

    # compute the similarity between the two images
    (score, diff) = structural_similarity(b_gray, a_gray, full=True)
    diff = (diff * 255).astype("uint8")

    if score < 0.99:
        # threshold the difference image
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        # The boundaries for cropping the image
        x_min = b_img.shape[1]//2
        y_min = b_img.shape[0]//2
        x_max = 0
        y_max = 0

        # compute the bounding box of the contour and then draw colored
        # bounding boxes on the before and after images
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:
                (x, y, w, h) = cv2.boundingRect(contour)
                b_img_canny = cv2.Canny(b_img[y: y + h, x: x + w], 50, 150)
                a_img_canny = cv2.Canny(a_img[y: y + h, x: x + w], 50, 150)
                sum_before = sum(sum(b_img_canny))
                sum_after = sum(sum(a_img_canny))

                if sum_after > 10:  # if something written in the specific box
                    is_something_written = True
                    if x < x_min:
                        x_min = x
                    if y < y_min:
                        y_min = y
                    if x + w > x_max:
                        x_max = x + w
                    if y + h > y_max:
                        y_max = y + h

                    if sum_before < 10:     # the area was empty before writing - green box
                        cv2.rectangle(b_img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.rectangle(a_img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    else:   # the area was not empty before writing - yellow box
                        cv2.rectangle(b_img_copy, (x, y), (x + w, y + h), (0, 255, 255), 2)
                        cv2.rectangle(a_img_copy, (x, y), (x + w, y + h), (0, 255, 255), 2)

                        # save the last board and create new one
                        is_new_board_added, counter, board = create_new_board(option, is_new_board_added, counter, board)

                else:   # erasing - red box
                    cv2.rectangle(b_img_copy, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.rectangle(a_img_copy, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    is_new_board_added, counter, board = create_new_board(option, is_new_board_added, counter, board)

                # show before-after images
                images_union = np.concatenate((a_img_copy,  b_img_copy), axis=1)
                images_union = cv2.resize(images_union, (images_union.shape[1] // 2, images_union.shape[0] // 2))
                cv2.imshow('Lesson', images_union)
                cv2.waitKey(100)
        cv2.waitKey(2000)

        if is_something_written:
            cut = a_img[y_min:y_max, x_min:x_max]

            if option is Const.SEPARATE_OPTION:
                cv2.imshow("Was cut from the board", cv2.resize(cut, (cut.shape[1] // 2, cut.shape[0] // 2)))
                cv2.imwrite("Output/Part%d.jpg" % counter, cut)
                counter += 1

            elif option is Const.APPEND_OPTION:
                board[y_min:y_max, x_min:x_max] = cut
                cv2.imshow("Added to the board", cv2.resize(board, (board.shape[1] // 2, board.shape[0] // 2)))

        cv2.waitKey(1000)
        cv2.destroyAllWindows()
    return counter, board
