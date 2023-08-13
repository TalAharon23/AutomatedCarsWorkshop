import cv2
import numpy as np

import Data_Structures

def Find_Parking_Slots(frame, matrix, frameSize, val_dict, parking_slots):
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds of the green color
    # lower_green = np.array([36, 25, 25])
    # upper_green = np.array([86, 255, 255])
    # Define the lower and upper bounds of the red color
    lower_red = np.array([0, 100, 100])  # Adjust these values based on the specific shade of red you want to detect
    upper_red = np.array([10, 255, 255])  # This range covers the hues near red

    # Threshold the image to get only the green color
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Find contours in the binary image
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort the contours by area in descending order
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Find the bounding rectangles of the largest 5 contours
    rects = []
    for cnt in contours[:10]:
        # Approximate the contour as a polygon
        epsilon = 0.01*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)

        # Find the bounding rectangle of the polygon
        x,y,w,h = cv2.boundingRect(approx)

        # Add the rectangle to the list if its area is larger than 10000 (i.e. it is clear)
        if w * h > 10000:# and w * h < 8000:
            rects.append((x, y, w, h))
            parking_slots.save_slot((x + int(round((w/2))), y + int(round(h/2))))


        for i in range(x, x + w):
            for j in range(y, y + h):
                if (x + w) <= 500 and (y + h) <= 700:
                    matrix[j][i] = Data_Structures.Val_dict.PARKING_SLOT


    # Draw a rectangle around each bounding rectangle
    for rect in rects:
        x, y, w, h = rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

    # Return the processed frame and the matrix
    return frame, matrix
