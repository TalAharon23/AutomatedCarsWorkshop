import cv2
import numpy as np
from scipy.spatial import distance
import Data_Structures

upside_left_corner = (0, 0)
white_avg_intensity_bottom = red_avg_intensity_top = 150
red_avg_intensity_bottom = 150
angle_diff_sensitivity = 15
pairs_distance_sensitivity = 15

def Find_Car(frame, matrix, frameSize, car):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.rectangle(gray, (150, 400), (150 + 70, 400 + 10), (255), 2)
    # output_adapthresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 51, 0)
    # kernel = np.ones((3, 3), np.uint8)
    # output_erosion = cv2.erode(output_adapthresh, kernel, iterations = 12)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Reduce threshold to increase white noise
    threshold1 = 80
    threshold2 = 100
    edges = cv2.Canny(blurred, threshold1, threshold2)
    cv2.imshow("test", edges)
    # Find contours in the dilated image
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # rect = cv2.minAreaRect(contours[0])
    # box = cv2.boxPoints(rect)
    # box = np.int0(box)
    # cv2.drawContours(frame, [box], 0, (100, 100, 100), 2)

    # Filter the contours to find the red strips for the forward and black strips for the backward


    if contours is not None:
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            # perimeter = cv2.arcLength(contour, False)
            approx = cv2.approxPolyDP(contour, 1.1 * perimeter, True)
            x, y, w, h = cv2.boundingRect(contour)
            if len(approx) > 0 and len(approx) < 50: # and ((w > 25 and h < 25) or (h > 25 and w < 25)):
                # Check if the strip is red or black based on its average intensity

                box = cv2.minAreaRect(contour)
                box = cv2.boxPoints(box)
                # box = np.array(box, dtype="int")
                box = np.int0(box)
                cv2.drawContours(frame, [box], 0, (100, 100, 100), 2)

                (top_left, top_right, bottom_right, bottom_left) = box

                distance_a = distance.euclidean((top_left[0], top_left[1]), (top_right[0], top_right[1]))
                distance_b = distance.euclidean((top_left[0], top_left[1]), (bottom_left[0], bottom_left[1]))

                dimension_a = distance_a / pixelsPerMm
                dimension_b = distance_b / pixelsPerMm

                length = max(dimension_a, dimension_b)
                width = min(dimension_a, dimension_b)
                # if length < 1 or length > 50:
                #     continue
                # if width < 1 or width > 40:
                #     continue
                # if width * length < 25:
                #     continue

                rice = [box.astype("int")]
                white_rices = []
                black_rices = []
                # Check class
                strip_roi = gray[y:y+h, x:x+w]
                avg_intensity = np.mean(strip_roi)
                if avg_intensity > white_avg_intensity_bottom:
                    white_rices.append({'class': 'class1', 'box': rice, 'color': (255, 255, 255), 'width': width, 'color_name': 'white',
                                  'top_right': top_right, 'contour' : contour})
                else:
                    black_rices.append({'class': 'class3', 'box': rice, 'color': (0, 0, 0), 'width': width, 'color_name': 'black',
                                  'top_right': top_right, 'contour': contour})

                cv2.putText(frame, "{:}".format('Front'),
                            (box[0][0] - 10, box[2][0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                            (255, 255, 255), 1)




        # if angle_degrees < 0:
        #     angle_degrees += 360
        # car.set_position(get_white_strip_rice(robot_rices))
        # car.set_direction_degrees(int(round(angle_degrees)))
        # print(int(round(angle_degrees)))
        # cv2.putText(frame, "{:}".format('Front'),
        #             (boundries[0][0] - 10, boundries[2][0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
        #             (255, 255, 255), 1)


    return matrix, frame

def find_pairs(paired_rices, rices):
    pass
    # Find paired strips from the same color

def calculate_angle_difference(contour1, contour2):
    # Find the bounding rectangles of the contours
    rect1 = cv2.minAreaRect(contour1)
    rect2 = cv2.minAreaRect(contour2)

    # Get the angles of the bounding rectangles
    angle1 = rect1[2]
    angle2 = rect2[2]

    # Calculate the absolute difference in angles
    angle_diff = abs(angle1 - angle2)

    # Normalize the angle difference to the range of [0, 180]
    angle_diff = angle_diff % 180

    # Take the minimum angle difference between the original and complement angles
    angle_diff = min(angle_diff, 180 - angle_diff)

    return angle_diff

def find_robot(robot_rices, rices):
    pass
            # break

def get_white_strip_rice(robot_rices):
    # strip_1_color = robot_rices[0]
    strip_1 = None
    strip_2 = None

    for rice in robot_rices[0]:
        if rice[0]['color_name'] == 'white':
            strip_1 = rice[0]
        elif rice[0]['color_name'] == 'black':
            strip_2 = rice[0]

    return (round((strip_1['box'][0][0][0] + strip_1['box'][0][1][0]) / 2), round(((strip_1['box'][0][0][1] + strip_1['box'][0][1][1]) / 2)))


def get_bounding_box(pairs):
    all_points = np.concatenate([pair for pair in pairs], axis=0)
    min_x = np.min(all_points[:, 0])
    min_y = np.min(all_points[:, 1])
    max_x = np.max(all_points[:, 0])
    max_y = np.max(all_points[:, 1])

    bounding_box = [[min_x, min_y], [max_x, max_y], [max_x, min_y], [min_x, max_y]]
    return bounding_box

def find_center(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    return (center_x, center_y)


def calculate_actual_angle_difference(robot_rices, curr_angle):
    # strip_1_color = robot_rices[0]
    strip_1 = None
    strip_2 = None

    for rice in robot_rices[0]:
        if rice[0]['color_name'] == 'white':
            strip_1 = rice[0]
        elif rice[0]['color_name'] == 'black':
            strip_2 = rice[0]

    # print(strip_1['box'][0][0][0])
    # print(strip_2['box'][0][0][0])
    # print(strip_1['box'][0][0][1])
    # print(strip_2['box'][0][0][1])

    if strip_1['box'][0][0][0] < strip_2['box'][0][0][0] and strip_1['box'][0][0][1] < strip_2['box'][0][0][1]:
        print(f"{curr_angle} + 270 = {curr_angle + 270}") #fix
        return curr_angle + 270
    elif strip_1['box'][0][0][0] < strip_2['box'][0][0][0] and strip_1['box'][0][0][1] > strip_2['box'][0][0][1]:
        print(f"{curr_angle} + 180 = {curr_angle + 180}") #fix
        return curr_angle + 180
    elif strip_1['box'][0][0][0] > strip_2['box'][0][0][0] and strip_1['box'][0][0][1] < strip_2['box'][0][0][1]:
        print(f"{curr_angle} + 0 = {curr_angle + 0}") #fix
        return curr_angle + 0
    else:
        print(f"{curr_angle} + 90 = {curr_angle + 90}") #fix
        return curr_angle + 90
