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
    rect = cv2.minAreaRect(contours[0])
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(frame, [box], 0, (100, 100, 100), 2)

    # Filter the contours to find the red strips for the forward and black strips for the backward
    red_strips = []
    white_strips = []
    black_strips = []
    if contours is not None:
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            if (w > 50 and h < 40) or (h > 50 and w < 40):
                # Check if the strip is red or black based on its average intensity
                strip_roi = gray[y:y+h, x:x+w]
                avg_intensity = np.mean(strip_roi)
                if avg_intensity > 210:
                    white_strips.append((x, y, w, h))
                elif avg_intensity > 120 and avg_intensity < 210:
                    red_strips.append((x, y, w, h))
                else:
                    black_strips.append((x, y, w, h))

    paired_strips = []
    # Find paired red strips
    find_pairs(paired_strips, red_strips)
    # Find paired black strips
    find_pairs(paired_strips, black_strips)
    # Find paired white strips
    find_pairs(paired_strips, white_strips)

    # Draw rectangles around the paired red strips
    for strip in paired_strips:
        x, y, w, h = strip
        if x > 3 and y > 3:
            cv2.rectangle(frame, (x - 3, y - 3), (x + w + 3, y + h + 3), (255, 255, 255), 2)
            cv2.rectangle(matrix, (x - 3, y - 3), (x + w + 3, y + h + 3), (255), 2)
        else:
            cv2.rectangle(frame, (x, y), (x + w + 3, y + h + 3), (255, 255, 255), 2)
            cv2.rectangle(matrix, (x, y), (x + w + 3, y + h + 3), (255), 2)


    # Draw rectangles around the black strips
    for strip in black_strips:
        x, y, w, h = strip
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 2)
        cv2.rectangle(matrix, (x, y), (x + w, y + h), (0), 2)
    for strip in red_strips:
        x, y, w, h = strip
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.rectangle(matrix, (x, y), (x + w, y + h), (0), 2)
    for strip in white_strips:
        x, y, w, h = strip
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(matrix, (x, y), (x + w, y + h), (0), 2)
    cv2.rectangle(frame, (150, 400), (150 + 80, 400 + 30), (0, 0, 0), 2)
    # Return the frame with the rectangles drawn around the strips
    return matrix, frame

def find_pairs(paired_strips, strips):
    # Find paired strips from the same color
    for i in range(len(strips)):
        strip1 = strips[i]
        for j in range(i + 1, len(strips)):
            strip2 = strips[j]
            if abs(strip1[1] - strip2[1]) < 50 or abs(strip1[0] - strip2[0]) < 50:  # Check if the coordinates are close
                paired_strips.append(strip1)
                paired_strips.append(strip2)
                break
