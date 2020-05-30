import cv2
import imutils
import numpy as np
import Const
from skimage.metrics import structural_similarity


def scan_board(b_img, a_img, counter, case, board):
    is_written = False
    is_new_board_added = False
    a_img = cv2.resize(a_img, (b_img.shape[1], b_img.shape[0]))
    gray_b = cv2.cvtColor(b_img, cv2.COLOR_RGB2GRAY)
    gray_a = cv2.cvtColor(a_img, cv2.COLOR_RGB2GRAY)
    gray_b = cv2.GaussianBlur(gray_b, (5, 5), 1)
    gray_a = cv2.GaussianBlur(gray_a, (5, 5), 1)

    a_img_copy = a_img.copy()
    b_img_copy = b_img.copy()
    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = structural_similarity(gray_b, gray_a, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))
    if score < 0.99:
        # threshold the difference image, followed by finding contours to
        # obtain the regions of the two input images that differ
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        x_min = Const.WIDTH_FRAME
        y_min = Const.HEIGHT_FRAME
        x_max = 0
        y_max = 0

        # loop over the contours
        for c in cnts:
            # compute the bounding box of the contour and then draw the
            # bounding box on both input images to represent where the two
            # images differ
            area = cv2.contourArea(c)
            if area > 100:
                (x, y, w, h) = cv2.boundingRect(c)
                img_canny_b = cv2.Canny(b_img[y: y + h, x: x + w], 50, 150)
                sum_before = sum(sum(img_canny_b))
                print("Before: ", str(sum_before))
                img_canny_a = cv2.Canny(a_img[y: y + h, x: x + w], 50, 150)
                sum_after = sum(sum(img_canny_a))
                print("After: ", str(sum_after))
                # case writing
                if sum_after > 10:
                    is_written = True
                    if x < x_min:
                        x_min = x
                    if y < y_min:
                        y_min = y
                    if x + w > x_max:
                        x_max = x + w
                    if y + h > y_max:
                        y_max = y + h
                    # writing on empty board
                    if sum_before < 10:
                        cv2.rectangle(b_img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.rectangle(a_img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # writing on nonempty board
                    else:
                        cv2.rectangle(b_img_copy, (x, y), (x + w, y + h), (0, 255, 255), 2)
                        cv2.rectangle(a_img_copy, (x, y), (x + w, y + h), (0, 255, 255), 2)
                        if case is Const.APPEND_CASE and not is_new_board_added:
                            is_new_board_added = True
                            cv2.imwrite("Output/Board%d.jpg" % counter, board)
                            board = np.full((board.shape[0], board.shape[1], 3), 125, dtype=np.uint8)
                            counter += 1

                # case erasing
                else:
                    cv2.rectangle(b_img_copy, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.rectangle(a_img_copy, (x, y), (x + w, y + h), (0, 0, 255), 2)

                img_u = np.concatenate((a_img_copy,  b_img_copy), axis=1)
                img_u = cv2.resize(img_u, (img_u.shape[1] // 2, img_u.shape[0] // 2))
                cv2.imshow('Lesson', img_u)
                # cv2.imshow("Lesson", cv2.resize(a_img_copy, (a_img_copy.shape[1] // 2, a_img_copy.shape[0] // 2)))
                # cv2.imshow("Before", cv2.resize(b_img_copy, (b_img_copy.shape[1] // 2, b_img_copy.shape[0] // 2)))
                cv2.waitKey(100)
        cv2.waitKey(2000)
        # show the output images
        # cv2.imshow("Lesson", cv2.resize(a_img_copy, (a_img_copy.shape[1] // 2, a_img_copy.shape[0] // 2)))
        # cv2.imshow("Lesson_b", cv2.resize(b_img_copy, (b_img_copy.shape[1] // 2, b_img_copy.shape[0] // 2)))
        # cv2.imshow("Diff", diff)
        # cv2.imshow("Thresh", thresh)

        if is_written:
            cut = a_img[y_min:y_max, x_min:x_max]

            if case is Const.SEPARATE_CASE:
                cv2.imshow("Was cut from the board", cv2.resize(cut, (cut.shape[1] // 2, cut.shape[0] // 2)))
                cv2.imwrite("Output/Part%d.jpg" % counter, cut)
                counter += 1

            elif case is Const.APPEND_CASE:
                board[y_min:y_max, x_min:x_max] = cut
                cv2.imshow("Added to the board", cv2.resize(board, (board.shape[1] // 2, board.shape[0] // 2)))

        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return counter, board

