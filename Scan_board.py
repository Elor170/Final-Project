import cv2
import imutils
from skimage.metrics import structural_similarity
import Constants


def scan_board(b_img, a_img, counter, case, board):
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
            if area > 100:
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(b_img_copy, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.rectangle(a_img_copy, (x, y), (x + w, y + h), (0, 0, 255), 2)
                if x < x_min:
                    x_min = x
                if y < y_min:
                    y_min = y
                if x + w > x_max:
                    x_max = x + w
                if y + h > y_max:
                    y_max = y + h

                # cv2.imshow("Before", cv2.threshold(gray_b[y: y+h, x: x+w], 127, 255, cv2.THRESH_BINARY))
                # cv2.imshow("After", cv2.threshold(gray_a[y: y+h, x: x+w], 127, 255, cv2.THRESH_BINARY))
                # print("Before", sum(sum(gray_b[y: y+h, x: x+w])), "\nAfter:", sum(sum(gray_a[y: y+h, x: x+w])))
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
        # show the output images
        # cv2.imshow("Original", gray_b)
        # cv2.imshow("Modified", gray_a)
        # cv2.imshow("Diff", diff)
        # cv2.imshow("Thresh", thresh)

        cv2.imshow("Lesson", cv2.resize(a_img_copy, (a_img_copy.shape[1] // 2, a_img_copy.shape[0] // 2)))
        cv2.imshow("Lesson_b", cv2.resize(b_img_copy, (b_img_copy.shape[1] // 2, b_img_copy.shape[0] // 2)))

        cut = a_img[y_min:y_max, x_min:x_max]

        if case is Constants.SEPARATE_CASE:
            cv2.imshow("Cut", cv2.resize(cut, (cut.shape[1] // 2, cut.shape[0] // 2)))
            cv2.imwrite("Output/Board%d.jpg" % counter, cut)
            counter += 1

        if case is Constants.APPEND_CASE:
            board[y_min:y_max, x_min:x_max] = cut
            cv2.imshow("Added to board", board)

        # cv2.waitKey(2000)
        cv2.destroyAllWindows()
    return counter, board

