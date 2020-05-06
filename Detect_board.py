
import cv2
import numpy as np

###################################
widthImg = 700
heightImg = 480
#####################################

cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('Resources/Lesson5.avi')
# cap.set(10, 150)
imgContour = None


def pre_processing(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)
    img_canny = cv2.Canny(img_blur, 200, 200)
    # cv2.imshow("imgCanny", img_canny)
    kernel = np.ones((5, 5))
    img_dial = cv2.dilate(img_canny, kernel, iterations=2)
    # cv2.imshow("imgDial", img_dial)
    img_thresh = cv2.erode(img_dial, kernel, iterations=1)
    # cv2.imshow("img_thresh", img_thresh)
    # cv2.waitKey(0)
    return img_thresh


def get_contours(img):
    biggest = np.array([])
    max_area = 0
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:
            # cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 20)
    return biggest


def reorder(my_points):
    my_points = my_points.reshape((4, 2))
    my_points_new = np.zeros((4, 1, 2), np.int32)
    add = my_points.sum(1)
    # print("add", add)
    my_points_new[0] = my_points[np.argmin(add)]
    my_points_new[3] = my_points[np.argmax(add)]
    diff = np.diff(my_points, axis=1)
    my_points_new[1] = my_points[np.argmin(diff)]
    my_points_new[2] = my_points[np.argmax(diff)]
    # print("NewPoints",myPointsNew)
    return my_points_new


def get_warp(img, biggest):
    biggest = reorder(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    img_output = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
    img_cropped = img_output[20:img_output.shape[0] - 20, 20:img_output.shape[1] - 20]
    img_cropped = cv2.resize(img_cropped, (widthImg, heightImg))
    return img_cropped, biggest


def stack_images(scale, img_array):
    rows = len(img_array)
    cols = len(img_array[0])
    rows_available = isinstance(img_array[0], list)
    width = img_array[0][0].shape[1]
    height = img_array[0][0].shape[0]
    if rows_available:
        for x in range(0, rows):
            for y in range(0, cols):
                if img_array[x][y].shape[:2] == img_array[0][0].shape[:2]:
                    img_array[x][y] = cv2.resize(img_array[x][y], (0, 0), None, scale, scale)
                else:
                    img_array[x][y] = cv2.resize(img_array[x][y], (img_array[0][0].shape[1], img_array[0][0].shape[0]),
                                                 None, scale, scale)
                if len(img_array[x][y].shape) == 2: img_array[x][y] = cv2.cvtColor(img_array[x][y], cv2.COLOR_GRAY2BGR)
        image_blank = np.zeros((height, width, 3), np.uint8)
        hor = [image_blank] * rows
        hor_con = [image_blank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(img_array[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if img_array[x].shape[:2] == img_array[0].shape[:2]:
                img_array[x] = cv2.resize(img_array[x], (0, 0), None, scale, scale)
            else:
                img_array[x] = cv2.resize(img_array[x], (img_array[0].shape[1], img_array[0].shape[0]), None, scale,
                                          scale)
            if len(img_array[x].shape) == 2: img_array[x] = cv2.cvtColor(img_array[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(img_array)
        ver = hor
    return ver


def detect_board(img):
    img_warped = 0
    coordinates = 0
    img_contour = img.copy()
    img_thresh = pre_processing(img)
    biggest = get_contours(img_thresh)
    if biggest.size != 0:
        img_warped, coordinates = get_warp(img, biggest)
        # image_array = ([img,img_thresh],
        #
        #           [img_contour,img_warped])
        image_array = ([img_contour, img_warped])
        # cv2.imshow("ImageWarped", img_warped)
    else:
        # image_array = ([img, img_thresh],
        #               [img, img])
        image_array = ([img_contour, img])

    stacked_images = stack_images(0.6, image_array)
    # cv2.imshow("WorkFlow", stacked_images)
    return img_warped, coordinates
