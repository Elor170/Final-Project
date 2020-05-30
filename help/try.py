import cv2
import numpy as np
import Const
from Detect_board import get_contours
from Detect_board import reorder


def empty(val):
    pass

# video source
path = '../Resources/Lesson_1.mp4'
cap = cv2.VideoCapture(path)
cv2.namedWindow("Image")
cv2.createTrackbar("Min_TB", 'Image', 0, 255, empty)
cv2.createTrackbar("Max_TB", 'Image', 0, 255, empty)


while True:
    min_threshold = cv2.getTrackbarPos("Min_TB", "Image")
    max_threshold = cv2.getTrackbarPos("Max_TB", "Image")
    success, img = cap.read()

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)
    img_canny = cv2.Canny(img_blur, min_threshold, max_threshold)
    points = get_contours(img_canny)
    if points.size is not 0:
        points = reorder(points)

        last_p = 0
        for p in points:
            if last_p is not 0:
                cv2.line(img, (p[0][0], p[0][1]), (last_p[0][0], last_p[0][1]), (0, 255, 0), 2)
            cv2.circle(img, (p[0][0], p[0][1]), 2, (0, 0, 255), -1)
            last_p = p
    else:
        cv2.circle(img, (100, 100), 50, (0, 0, 255), -1)
    img_u = np.concatenate((img, cv2.cvtColor(img_canny, cv2.COLOR_GRAY2BGR)), axis=1)
    img_u = cv2.resize(img_u, (img_u.shape[1] // 2, img_u.shape[0] // 2))
    cv2.imshow('Image', img_u)

    if cv2.waitKey(1) & 0xFF == Const.ESC_KEY_BOARD:
        break

cv2.destroyAllWindows()
