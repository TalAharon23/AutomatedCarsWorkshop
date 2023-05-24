import cv2
import numpy as np


def Find_Car(frame, matrix, frameSize):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Threshold the grayscale image to create a binary image
    _, thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)

    # Dilate the binary image to fill in any gaps
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilated = cv2.dilate(thresh, kernel, iterations=2)

    # Find contours in the dilated image
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter the contours to find the white plus
    if contours is not None:
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            if 0.7 < aspect_ratio < 1.3 and w > 30 and h > 30:
                # Draw a green rectangle around the white plus
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Draw the line on the matrix
                cv2.rectangle(matrix, (x, y), (x + w, y + h), (255), 2)
                break

    # Return the frame with the green rectangle drawn around the white plus
    return matrix, frame
