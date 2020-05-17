import cv2
import numpy as np
import Constants


def pre_processing(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)
    img_canny = cv2.Canny(img_blur, 200, 200)
    # cv2.imshow("Canny", cv2.resize(img_canny, (img_canny.shape[1]//2, img_canny.shape[0]//2)))
    kernel = np.ones((5, 5))
    img_dial = cv2.dilate(img_canny, kernel, iterations=2)
    img_thresh = cv2.erode(img_dial, kernel, iterations=1)
    # cv2.imshow("Thresh", cv2.resize(img_thresh, (img_thresh.shape[1] // 2, img_thresh.shape[0] // 2)))
    return img_thresh


def get_contours(img):
    biggest_points = np.array([])
    max_area = 0
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > (Constants.WIDTH_FRAME * Constants.HEIGHT_FRAME / 5):
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest_points = approx
                max_area = area
    return biggest_points


def reorder(my_points):
    my_points = my_points.reshape((4, 2))
    my_points_new = np.zeros((4, 1, 2), np.int32)
    add = my_points.sum(1)
    my_points_new[0] = my_points[np.argmin(add)]
    my_points_new[3] = my_points[np.argmax(add)]
    diff = np.diff(my_points, axis=1)
    my_points_new[1] = my_points[np.argmin(diff)]
    my_points_new[2] = my_points[np.argmax(diff)]
    return my_points_new


def get_warp(img, new_c):
    pts_src = np.float32(new_c)
    # for p in pts_src:
    #     print(sum(sum(new_c)))
    #     cv2.circle(img, (p[0][0], p[0][1]), 1, (0, 0, 255))
    (x, y, w, h) = cv2.boundingRect(new_c)
    pts_dst = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv2.getPerspectiveTransform(pts_src, pts_dst)
    img_warped = cv2.warpPerspective(img, matrix, (w, h))
    img_cropped = img_warped[5: h-5, 5: w-5]
    return img_cropped


def detect_board(img):
    img_warped = img.copy()
    img_thresh = pre_processing(img)
    new_coordinates = get_contours(img_thresh)
    # not while writing
    if new_coordinates.size != 0:
        is_writing = False
        new_coordinates = reorder(new_coordinates)
        img_warped = get_warp(img, new_coordinates)
    # while write
    else:
        is_writing = True
    return img_warped, is_writing
