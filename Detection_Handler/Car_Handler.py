import cv2
import numpy as np

def Find_Car(frame, matrix, frameSize):
    # Convert the image to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the image to isolate the yellow color
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    # cv2.imshow('Image', mask)

    # Apply morphological operations to the thresholded image
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)
    mask = cv2.dilate(mask, kernel)

    # Detect circles in the thresholded image
    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 200)

    # Draw circles around the detected yellow circles
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(mask, (x, y), r, (0, 255, 0), 2)

    # Display the image with the detection results
    cv2.imshow('Image', mask)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return matrix, frame






