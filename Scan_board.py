import cv2
from skimage.measure import compare_ssim
import imutils
import Constants
import argparse
import numpy as np


def scan_board(b_img, a_img, num):
    gray_b = cv2.cvtColor(b_img, cv2.COLOR_RGB2GRAY)
    gray_a = cv2.cvtColor(a_img, cv2.COLOR_RGB2GRAY)
    # gray_b = cv2.GaussianBlur(gray_b, (5, 5), 2)
    # gray_a = cv2.GaussianBlur(gray_a, (5, 5), 2)
    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(gray_b, gray_a, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))
    if score < 0.97:
        # threshold the difference image, followed by finding contours to
        # obtain the regions of the two input images that differ
        thresh = cv2.threshold(diff, 0, 255,
                               cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
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
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(gray_b, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(gray_a, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # if h > 30 and w > 30:
            #     if x < x_min:
            #         x_min = x
            #     if y < y_min:
            #         y_min = y
            #     if x > x_max:
            #         x_max = y
            #     if y > y_max:
            #         y_max = y

        # show the output images
        cv2.imshow("Original", gray_b)
        cv2.imshow("Modified", gray_a)
        cv2.imshow("Diff", diff)
        cv2.imshow("Thresh", thresh)
        # (x, y, w, h) = cv2.boundingRect(thresh)
        # write the output
        # print(x, y, w, h)
        # output = a_img[x:x+w, y:y+h, :]
        # cv2.imshow("Output", output)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
