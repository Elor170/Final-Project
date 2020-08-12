import cv2
import Const
import numpy as np


def pre_processing(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)
    img_canny = cv2.Canny(img_blur, 200, 200)
    img_threshold = cv2.dilate(img_canny, Const.KERNEL, iterations=3)
    return img_threshold


def get_coordinates(img):
    img_space: int = img.shape[0] * img.shape[1]
    biggest_points: np.ndarray = np.array([])
    max_area: int = 0
    contours: list
    hierarchy: np.ndarray
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        area: float = cv2.contourArea(contour)
        if area > (img_space / 5):
            peri: float = cv2.arcLength(contour, True)
            approx: np.ndarray = cv2.approxPolyDP(contour, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest_points: np.ndarray = approx
                max_area: float = area

    return biggest_points


def reorder(points):
    points: np.ndarray = points.reshape((4, 2))
    add: np.ndarray = points.sum(1)
    diff: np.ndarray = np.diff(points, axis=1)
    reordered_points: np.ndarray = np.zeros((4, 1, 2), np.int32)

    reordered_points[0] = points[np.argmin(add)]
    reordered_points[1] = points[np.argmin(diff)]
    reordered_points[2] = points[np.argmax(diff)]
    reordered_points[3] = points[np.argmax(add)]
    return reordered_points


def get_warp(img, coordinates):
    (x, y, w, h) = cv2.boundingRect(coordinates)
    points_src = np.float32(coordinates)
    points_dst = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv2.getPerspectiveTransform(points_src, points_dst)
    img_warped = cv2.warpPerspective(img, matrix, (w, h))
    img_cropped = img_warped[10: h-10, 10: w-10]
    return img_cropped


def detect_board(img):
    img_thresh = pre_processing(img)
    coordinates = get_coordinates(img_thresh)

    # not while writing
    if coordinates.size != 0:
        is_writing = False
        coordinates = reorder(coordinates)
        img_warped = get_warp(img, coordinates)

    # while write
    else:
        is_writing = True
        img_warped = img.copy()

    return img_warped, is_writing
