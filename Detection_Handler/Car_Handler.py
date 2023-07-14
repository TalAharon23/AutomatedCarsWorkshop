import cv2
import numpy as np
from scipy.spatial import distance

class contour_data:
    def __init__(self, width, length, color_name, rice):
        self.width = width
        self.length = length
        self.color_name = color_name
        self.rice = rice

def Find_Car(frame, matrix, frameSize):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.rectangle(gray, (150, 400), (150 + 70, 400 + 10), (255), 2)


    # # Threshold the grayscale image to create a binary image
    # _, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    #
    # # Dilate the binary image to fill in any gaps
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    # dilated = cv2.dilate(thresh, kernel, iterations=2)


    output_adapthresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 51, 0)

    kernel = np.ones((3, 3), np.uint8)
    # output_erosion = cv2.erode(output_adapthresh, kernel, iterations = 12)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Reduce threshold to increase white noise
    threshold1 = 120
    threshold2 = 150
    edges = cv2.Canny(blurred, threshold1, threshold2)
    cv2.imshow("test", edges)
    # Find contours in the dilated image
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rect = cv2.minAreaRect(contours[0])
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(frame, [box], 0, (100, 100, 100), 2)

    # Filter the contours to find the red strips for the forward and black strips for the backward
    red_rices = []
    white_rices = []
    black_rices = []
    paired_rices = []
    pixelsPerMm = 5.509
    rices = []

    if contours is not None:
        for contour in contours:
            perimeter = cv2.arcLength(contour, False)
            approx = cv2.approxPolyDP(contour, 0.9 * perimeter, False)
            x, y, w, h = cv2.boundingRect(contour)
            if len(approx) > 0 and len(approx) < 13: # and ((w > 25 and h < 25) or (h > 25 and w < 25)):
                # Check if the strip is red or black based on its average intensity

                box = cv2.minAreaRect(contour)
                box = cv2.boxPoints(box)
                box = np.array(box, dtype="int")

                (top_left, top_right, bottom_right, bottom_left) = box

                distance_a = distance.euclidean((top_left[0], top_left[1]), (top_right[0], top_right[1]))
                distance_b = distance.euclidean((top_left[0], top_left[1]), (bottom_left[0], bottom_left[1]))

                dimension_a = distance_a / pixelsPerMm
                dimension_b = distance_b / pixelsPerMm

                length = max(dimension_a, dimension_b)
                width = min(dimension_a, dimension_b)

                if length < 6 or length > 12.3:
                    continue
                if width < 2 or width > 3.5:
                    continue

                rice = [box.astype("int")]
                # # Check class
                # if avg_intensity > 160:
                #     rices.append({'class': 'class1', 'box': rice, 'color': (255, 255, 255), 'width': width,
                #                   'color_name': 'white',
                #                   'top_right': top_right})
                #     white_strips.append(contour)
                # elif avg_intensity > 92 and avg_intensity < 160:
                #     rices.append(
                #         {'class': 'class2', 'box': rice, 'color': (0, 0, 255), 'width': width, 'color_name': 'red',
                #          'top_right': top_right})
                #     red_strips.append(contour)
                # else:
                #     rices.append(
                #         {'class': 'class3', 'box': rice, 'color': (0, 0, 0), 'width': width, 'color_name': 'black',
                #          'top_right': top_right})
                #     black_strips.append(contour)

                # Check class
                strip_roi = gray[y:y+h, x:x+w]
                avg_intensity = np.mean(strip_roi)
                if avg_intensity > 160:
                    white_rices.append({'class': 'class1', 'box': rice, 'color': (255, 255, 255), 'width': width, 'color_name': 'white',
                                  'top_right': top_right})
                elif avg_intensity > 92 and avg_intensity < 160:
                    red_rices.append({'class': 'class2', 'box': rice, 'color': (0, 0, 255), 'width': width, 'color_name': 'red',
                                  'top_right': top_right})
                else:
                    black_rices.append({'class': 'class3', 'box': rice, 'color': (0, 0, 0), 'width': width, 'color_name': 'black',
                                  'top_right': top_right})

                # strip_roi = gray[y:y+h, x:x+w]
                # avg_intensity = np.mean(strip_roi)
                # if avg_intensity > 180:
                #     white_strips.append((x, y, w, h))
                # elif avg_intensity > 80 and avg_intensity < 180:
                #     red_strips.append((x, y, w, h))
                # else:
                #     black_strips.append((x, y, w, h))

    find_pairs(paired_rices=paired_rices, rices=red_rices)
    find_pairs(paired_rices=paired_rices, rices=black_rices)

    for paired_rice in paired_rices:
        cv2.drawContours(frame, paired_rice['box'], -1, paired_rice['color'], 1)
        cv2.drawContours(matrix, paired_rice['box'], -1, (255), 1)
        cv2.putText(frame, "{:}".format(paired_rice['color_name']),
                    (paired_rice['top_right'][0] - 10, paired_rice['top_right'][1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                    (255, 255, 255), 1)


    # # Find paired red strips
    # find_pairs(paired_strips, red_strips)
    # # Find paired black strips
    # find_pairs(paired_strips, black_strips)
    # # Find paired white strips
    # find_pairs(paired_strips, white_strips)


    cv2.rectangle(frame, (150, 400), (150 + 80, 400 + 10), (255, 255, 255), 2)
    # Return the frame with the rectangles drawn around the strips
    return matrix, frame

def find_pairs(paired_rices, rices):
    # Find paired strips from the same color
    for i in range(len(rices)):
        strip1 = rices[i]
        for j in range(i + 1, len(rices)):
            strip2 = rices[j]
            print(strip1['box'][0][0][0])
            if abs(strip1['box'][0][0][0] - strip2['box'][0][0][0]) < 10: # or abs(strip1['box'][0][1] - strip2['box'][0][1]) < 50\
                    # or abs(strip1['box'][1][0] - strip2['box'][1][0]) < 50 or abs(strip1['box'][1][1] - strip2['box'][1][1]) < 50:  # Check if the coordinates are close
                paired_rices.append(strip1)
                paired_rices.append(strip2)
                break
