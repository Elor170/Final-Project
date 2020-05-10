import cv2
from skimage.measure import compare_ssim
import imutils
import Constants
import numpy as np

board = np.full((Constants.HEIGHT_FRAME, Constants.WIDTH_FRAME, 3), 125, dtype=np.uint8)


def scan_board(b_img, a_img, counter, case):
    b_img_blur = cv2.GaussianBlur(b_img, (5, 5), 50, 50, 50)
    a_img_blur = cv2.GaussianBlur(a_img, (5, 5), 50, 50, 50)
    gray_b = cv2.cvtColor(b_img_blur, cv2.COLOR_RGB2GRAY)
    gray_a = cv2.cvtColor(a_img_blur, cv2.COLOR_RGB2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(gray_b, gray_a, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))
    if score < 0.99:

        # threshold the difference image, followed by finding contours to
        # obtain the regions of the two input images that differ
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        x_min = Constants.WIDTH_FRAME
        y_min = Constants.HEIGHT_FRAME
        x_max = 0
        y_max = 0

        # loop over the contours
        for c in cnts:
            # compute the bounding box of the contour and then draw the
            # bounding box on both input images to represent where the two
            # images differ
            area = cv2.contourArea(c)
            if area > 200:
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(gray_b, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.rectangle(gray_a, (x, y), (x + w, y + h), (0, 0, 255), 2)

                if x < x_min:
                    x_min = x
                if y < y_min:
                    y_min = y
                if x + w > x_max:
                    x_max = x + w
                if y + h > y_max:
                    y_max = y + h
        # show the output images
        # cv2.imshow("Original", gray_b)
        # cv2.imshow("Modified", gray_a)
        # cv2.imshow("Diff", diff)
        # cv2.imshow("Thresh", thresh)
        cv2.imshow("Lesson", gray_a)
        cv2.imshow("Lesson_b", gray_b)

        cut = a_img[y_min:y_max, x_min:x_max]

        if case is Constants.SEPARATE_CASE:
            cv2.imshow("Cut", cut)
            cv2.imwrite("Output/Board%d.jpg" % counter, cut)
            counter += 1

        if case is Constants.APPEND_CASE:
            board[y_min:y_max, x_min:x_max] = cut
            cv2.imshow("Added to board", board)

        cv2.waitKey(1000)
        cv2.destroyAllWindows()
    return counter, board

