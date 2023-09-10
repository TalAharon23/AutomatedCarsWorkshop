import cv2
import numpy as np

import Data_Structures


def Find_Lines(frame, matrix, frameSize, mask, val_dict):
    # Load the image
    # Reading the required image in
    # which operations are to be done.
    # Make sure that the image is in the same
    # directory in which this python program is
    # Read image
    # image = cv2.imread('Resources/Amir_Test/lines.jpg')
    image = frame
    line_color = (0, 255, 0)
    matrix_value = 0
    # Convert image to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper ranges for the color red
    # If the mask is Line.
    if mask == 'Path':
        lower_red = np.array([0, 50, 50])
        upper_red = np.array([10, 255, 255])
        lower_red2 = np.array([170, 50, 50])
        upper_red2 = np.array([180, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = mask1 + mask2
        matrix_value = 2

    elif mask == 'Border':
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        line_color = (255, 255, 0)  # Print different color for border lines.
        matrix_value = 1

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
        maxLineGap=60  # Max allowed gap between line for joining them
    )

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]

            # Draw the line on the matrix
            cv2.line(matrix, (x1, y1), (x2, y2), (255), 1)

            # Draw the lines joing the points
            # On the original image
            cv2.line(image, (x1, y1), (x2, y2), line_color, 2)
            # Maintain a simples lookup list for points
            lines_list.append([(x1, y1), (x2, y2)])

    # Save the result image
    return matrix, image
