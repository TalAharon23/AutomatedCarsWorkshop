import cv2
import numpy as np

def Find_Lines(frame, matrix, frameSize):
    # Load the image
    # Reading the required image in
    # which operations are to be done.
    # Make sure that the image is in the same
    # directory in which this python program is
    # Read image
    # image = cv2.imread('Resources/Amir_Test/lines.jpg')
    image = frame

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use canny edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Apply HoughLinesP method to
    # to directly obtain line end points
    lines_list = []
    lines = cv2.HoughLinesP(
        edges,  # Input edge image
        1,  # Distance resolution in pixels
        np.pi / 180,  # Angle resolution in radians
        threshold=80,  # Min number of votes for valid line
        minLineLength=10,  # Min allowed length of line
        maxLineGap=10  # Max allowed gap between line for joining them
    )

    # Iterate over points
    for points in lines:
        # Extracted points nested in the list
        x1, y1, x2, y2 = points[0]
        for iter_x in range(x2 - x1):
            for iter_y in range(y2 - y1):
                matrix[x1 + iter_x, y1 + iter_y] = 1 # Does not handle the cases that y2<y1 and x2<x1
        # Draw the lines joing the points
        # On the original image
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # Maintain a simples lookup list for points
        lines_list.append([(x1, y1), (x2, y2)])

    # Save the result image
    return matrix, image
    #
    # cv2.imshow("Detected lines", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
