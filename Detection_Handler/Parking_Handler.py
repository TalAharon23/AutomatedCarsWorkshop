import cv2
import numpy as np

import Data_Structures


x_parking_delta = 75
y_parking_delta = 160

def Find_Parking_Slots(frame, matrix, frameSize, val_dict, parking_slots):
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    box = None
    # Define the lower and upper bounds of the green color
    # lower_green = np.array([36, 25, 25])
    # upper_green = np.array([86, 255, 255])
    # Define the lower and upper bounds of the red color
    # lower_red = np.array([0, 100, 100])  # Adjust these values based on the specific shade of red you want to detect
    # upper_red = np.array([20, 255, 255])  # This range covers the hues near red
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    # Create masks for each red range
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # Combine the masks to get the final mask
    final_mask = cv2.bitwise_or(mask1, mask2)
    kernel = np.ones((5, 5), np.uint8)
    final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_OPEN, kernel)

    # Threshold the image to get only the green color
    # mask = cv2.inRange(hsv, lower_red, upper_red)

    # Find contours in the binary image
    contours, hierarchy = cv2.findContours(final_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort the contours by area in descending order
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Find the bounding rectangles of the largest 5 contours
    rects = []
    for cnt in contours: # [:100]:
        # Approximate the contour as a polygon
        # cnt = cv2.minAreaRect(cnt)

        epsilon = 0.01*cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,epsilon,True)

        box = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(box)
        # box = np.array(box, dtype="int")
        box = np.int0(box)

        # Find the bounding rectangle of the polygon
        x,y,w,h = cv2.boundingRect(approx)

        # Add the rectangle to the list if its area is larger than 10000 (i.e. it is clear)
        if w * h > 10000 and w * h < 36000:
            rects.append((x, y, w, h))
            rect = cv2.minAreaRect(cnt)
            angle = rect[2]
            parking_slots.save_slot_contours(cnt)
            parking_slots.save_slot(Data_Structures.Cell(x + int(round((w/2))) + x_parking_delta, y + int(round(h/2)) + y_parking_delta))
            cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
            if w > h:
                angle += 90
            else:
                angle += 180
            print(f"parking: {angle}")
            print(f"parking: {angle}")
            print(f"parking: {angle}")
            print(f"parking: {angle}")
            print(f"parking: {angle}")



            for i in range(x, x + w):
                for j in range(y, y + h):
                    matrix[j][i] = Data_Structures.Val_dict.PARKING_SLOT



    # # Draw a rectangle around each bounding rectangle
    # for rect in rects:
    #     x, y, w, h = rect
    #     cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)

    # Return the processed frame and the matrix
    return box, matrix
