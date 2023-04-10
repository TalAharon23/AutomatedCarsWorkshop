import cv2
import numpy as np



def Find_Lines(frame, matrix, frameSize, mask):
    # Load the image
    # Reading the required image in
    # which operations are to be done.
    # Make sure that the image is in the same
    # directory in which this python program is
    # Read image
    # image = cv2.imread('Resources/Amir_Test/lines.jpg')
    image = frame
    line_color = (0, 255, 0)

    # Convert image to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper ranges for the color red
    # If the mask is Line (the path the car travels on).
    # If the mask is Line.
    if mask == 'Path':
        lower_red = np.array([0, 50, 50])
        upper_red = np.array([10, 255, 255])
        lower_red2 = np.array([170, 50, 50])
        upper_red2 = np.array([180, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = mask1 + mask2

    elif mask == 'Border':
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        line_color = (255, 255, 0)  # Print different color for border lines.

    # Use canny edge detection
    edges = cv2.Canny(mask, 50, 150, apertureSize=3)

    # Apply HoughLinesP method to
    # to directly obtain line end points
    lines_list = []
    lines = cv2.HoughLinesP(
        edges,  # Input edge image
        1,  # Distance resolution in pixels
        np.pi / 180,  # Angle resolution in radians
        threshold=80,  # Min number of votes for valid line
        minLineLength=0,  # Min allowed length of line
        maxLineGap=4  # Max allowed gap between line for joining them
    )

    # Iterate over points
    if lines is not None:
        for points in lines:
            # Extracted points nested in the list
            x1, y1, x2, y2 = points[0]

            big_X = x2
            small_x = x1
            big_y = y2
            small_y = y1
            if x1 > x2:
                big_X = x1
                small_x = x2
            if y1 > y2:
                big_y = y1
                small_y = y2
            while small_y <= big_y and small_x <= big_X:
                matrix[small_x, small_y] = 1
                if small_x <= big_X:
                    small_x += 1
                if small_y <= big_y:
                    small_y += 1

            # for iter_x in range(big_X - small_x):
            #    for iter_y in range(big_y - small_y):
            #        matrix[small_x + iter_x, small_y + iter_y] = 1
            # Draw the lines joing the points
            # On the original image
            cv2.line(image, (x1, y1), (x2, y2), line_color, 2)
            # Maintain a simples lookup list for points
            lines_list.append([(x1, y1), (x2, y2)])

    # Save the result image
    return matrix, image




"""
import cv2
import numpy as np

def Find_Parking(frame, matrix, frameSize):
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds of the green color
    lower_green = np.array([36, 25, 25])
    upper_green = np.array([86, 255, 255])

    # Threshold the image to get only the green color
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours in the binary image
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the bounding rectangles of all the contours
    rects = [cv2.boundingRect(cnt) for cnt in contours]

    # Draw a rectangle around each bounding rectangle
    for rect in rects:
        x, y, w, h = rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Return the processed frame and the matrix
    return frame, matrix

----------------------------------
this is part is detecting only 1 rectangle
import cv2
import numpy as np


def Find_Parking(frame, matrix, frameSize):
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds of the green color
    lower_green = np.array([36, 25, 25])
    upper_green = np.array([86, 255, 255])

    # Threshold the image to get only the green color
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours in the binary image
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through the contours and find the rectangle with the largest area
    max_area = 0
    max_rect = None
    for cnt in contours:
        # Approximate the contour as a polygon
        epsilon = 0.01 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # Find the bounding rectangle of the polygon
        x, y, w, h = cv2.boundingRect(approx)

        # Calculate the area of the rectangle
        area = w * h

        # If the area is larger than the current maximum, update the maximum rectangle
        if area > max_area:
            max_area = area
            max_rect = (x, y, w, h)

    # Draw a rectangle around the maximum rectangle
    if max_rect is not None:
        x, y, w, h = max_rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Return the processed frame and the matrix
    return frame, matrix

"""



