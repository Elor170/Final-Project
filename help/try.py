import cv2
import numpy as np
import Const
from Detect_board import get_coordinates
from Detect_board import reorder


def empty(val):
    pass

# video source
path = '../im.jpg'
img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
#img = cv2.GaussianBlur(img, (5, 5), 1, 5, 1)
# img = cv2.blur(img, (3, 3))
kernel = np.ones((5, 5))

cv2.imshow("img", img)
cv2.waitKey(0)
# cv2.namedWindow("Image")
# cv2.createTrackbar("Min_Thresh", 'Image', 0, 255, empty)
# cv2.createTrackbar("Max_Thresh", 'Image', 0, 255, empty)
# cv2.createTrackbar("Distance", 'Image', 0, 255, empty)
# cv2.createTrackbar("Sigma_Color", 'Image', 0, 255, empty)
# cv2.createTrackbar("Sigma_Space", 'Image', 0, 255, empty)
#
#
# while True:
#     min_threshold = cv2.getTrackbarPos("Min_Thresh", "Image")
#     max_threshold = cv2.getTrackbarPos("Max_Thresh", "Image")
#     distance = cv2.getTrackbarPos("Distance", "Image")
#     sigma_color = cv2.getTrackbarPos("Sigma_Color", "Image")
#     sigma_space = cv2.getTrackbarPos("Sigma_Space", "Image")
#
#     b_img = cv2.bilateralFilter(img, distance, sigma_color, sigma_space)
#     _, t_img = cv2.threshold(img, min_threshold, max_threshold, cv2.THRESH_BINARY)
#     _, tb_img = cv2.threshold(b_img, min_threshold, max_threshold, cv2.THRESH_BINARY)
#     # cv2.imshow('img', img)
#     # cv2.imshow('b_img', b_img)
#     # cv2.imshow('t_img', t_img)
#     # cv2.imshow('tb_img', tb_img)
#
#     img_u = np.concatenate((img, t_img, b_img, tb_img), axis=1)
#     img_u = cv2.resize(img_u, (img_u.shape[1] // 2, img_u.shape[0] // 2))
#     cv2.imshow('I', img_u)
#
#     # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     # img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)
#     # img_canny = cv2.Canny(img_blur, min_threshold, max_threshold)
#     # points = get_contours(img_canny)
#     # if points.size is not 0:
#     #     points = reorder(points)
#     #
#     #     last_p = 0
#     #     for p in points:
#     #         if last_p is not 0:
#     #             cv2.line(img, (p[0][0], p[0][1]), (last_p[0][0], last_p[0][1]), (0, 255, 0), 2)
#     #         cv2.circle(img, (p[0][0], p[0][1]), 2, (0, 0, 255), -1)
#     #         last_p = p
#     # else:
#     #     cv2.circle(img, (100, 100), 50, (0, 0, 255), -1)
#     # img_u = np.concatenate((img, cv2.cvtColor(img_canny, cv2.COLOR_GRAY2BGR)), axis=1)
#     # img_u = cv2.resize(img_u, (img_u.shape[1] // 2, img_u.shape[0] // 2))
#     # cv2.imshow('Image', img_u)
#
#     if cv2.waitKey(1) & 0xFF == Const.ESC_KEY_BOARD:
#         break
# cv2.imwrite("out.jpg", tb_img)
# cv2.destroyAllWindows()

# show the output images- after 85
        # cv2.imshow("Lesson", cv2.resize(a_img_copy, (a_img_copy.shape[1] // 2, a_img_copy.shape[0] // 2)))
        # cv2.imshow("Lesson_b", cv2.resize(b_img_copy, (b_img_copy.shape[1] // 2, b_img_copy.shape[0] // 2)))
        # cv2.imshow("Diff", diff)
        # cv2.imshow("Thresh", thresh)
