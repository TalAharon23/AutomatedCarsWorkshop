import cv2
import numpy as np
from scipy.spatial import distance
import Data_Structures

upside_left_corner = (0, 0)
white_avg_intensity_bottom = red_avg_intensity_top = 130
red_avg_intensity_bottom = 130
angle_diff_sensitivity = 12
pairs_distance_sensitivity = 13

def Find_Car(frame, matrix, frameSize, car):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.rectangle(gray, (150, 400), (150 + 70, 400 + 10), (255), 2)
    # output_adapthresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 51, 0)
    # kernel = np.ones((3, 3), np.uint8)
    # output_erosion = cv2.erode(output_adapthresh, kernel, iterations = 12)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Reduce threshold to increase white noise
    threshold1 = 100
    threshold2 = 130
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
    robot_rices = []
    pixelsPerMm = 5.509
    rices = []

    if contours is not None:
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 1.1 * perimeter, True)
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
                if length < 4 or length > 15:
                    continue
                if width < 1 or width > 6:
                    continue

                rice = [box.astype("int")]

                # Check class
                strip_roi = gray[y:y+h, x:x+w]
                avg_intensity = np.mean(strip_roi)
                if avg_intensity > white_avg_intensity_bottom:
                    white_rices.append({'class': 'class1', 'box': rice, 'color': (255, 255, 255), 'width': width, 'color_name': 'white',
                                  'top_right': top_right, 'contour' : contour})
                elif avg_intensity > red_avg_intensity_bottom and avg_intensity < white_avg_intensity_bottom:
                    red_rices.append({'class': 'class2', 'box': rice, 'color': (0, 0, 255), 'width': width, 'color_name': 'red',
                                  'top_right': top_right, 'contour': contour})
                else:
                    black_rices.append({'class': 'class3', 'box': rice, 'color': (0, 0, 0), 'width': width, 'color_name': 'black',
                                  'top_right': top_right, 'contour': contour})

    find_pairs(paired_rices=paired_rices, rices=white_rices)
    find_pairs(paired_rices=paired_rices, rices=black_rices)

    for paired_rice in paired_rices:
        cv2.drawContours(frame, paired_rice[0]['box'], -1, paired_rice[0]['color'], 1)
        cv2.drawContours(matrix, paired_rice[0]['box'], -1, (255), 1)
        cv2.putText(frame, "{:}".format(paired_rice[0]['color_name']),
                    (paired_rice[0]['top_right'][0] - 10, paired_rice[0]['top_right'][1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                    (255, 255, 255), 1)
        cv2.drawContours(frame, paired_rice[1]['box'], -1, paired_rice[0]['color'], 1)
        cv2.drawContours(matrix, paired_rice[1]['box'], -1, (255), 1)
        cv2.putText(frame, "{:}".format(paired_rice[1]['color_name']),
                    (paired_rice[1]['top_right'][0] - 10, paired_rice[1]['top_right'][1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                    (255, 255, 255), 1)

    find_robot(robot_rices, paired_rices)
    for robot_rice in robot_rices:
        boundries = get_bounding_box(robot_rice[0][0]['box'])
        # Draws a rectangle on the front of the robot
        cv2.rectangle(frame, boundries[0], boundries[1], (0, 255, 0), 2)
        cv2.drawContours(matrix, robot_rice[0][0]['box'], -1, (255), 1)
        moment = cv2.moments(robot_rice[0][0]['contour'])
        centroid_x = int(moment["m10"] / moment["m00"])
        centroid_y = int(moment["m01"] / moment["m00"])
        contour_centroid = (centroid_x, centroid_y)
        dx = upside_left_corner[0] - contour_centroid[0]
        dy = upside_left_corner[1] - contour_centroid[1]
        # angle_radians = np.arctan2(dy, dx)
        # angle_degrees = np.degrees(angle_radians)
        rect1 = cv2.minAreaRect(robot_rice[0][0]['contour'])
        angle_degrees = rect1[2]
        angle_degrees = calculate_actual_angle_difference(robot_rices, angle_degrees)


        # if angle_degrees < 0:
        #     angle_degrees += 360
        car.set_position(get_white_strip_rice(robot_rices))
        car.set_direction_degrees(int(round(angle_degrees)))
        print(int(round(angle_degrees)))
        # cv2.putText(frame, "{:}".format('Front'),
        #             (boundries[0][0] - 10, boundries[2][0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
        #             (255, 255, 255), 1)



    # cv2.rectangle(frame, (400, 400), (400 + 30, 400 + 80), (255, 255, 255), 2)
    # Return the frame with the rectangles drawn around the strips
    return matrix, frame

def find_pairs(paired_rices, rices):
    # Find paired strips from the same color
    for i in range(len(rices)):
        strip1 = rices[i]
        for j in range(i + 1, len(rices)):
            strip2 = rices[j]
            if abs(strip1['box'][0][0][0] - strip2['box'][0][0][0]) < pairs_distance_sensitivity \
                    and abs(strip1['box'][0][1][0] - strip2['box'][0][1][0]) < pairs_distance_sensitivity\
                    and abs(strip1['box'][0][2][0] - strip2['box'][0][2][0]) < pairs_distance_sensitivity\
                    and abs(strip1['box'][0][3][0] - strip2['box'][0][3][0]) < pairs_distance_sensitivity\
                    and (strip1['color_name'] == strip2['color_name']): # or abs(strip1['box'][0][1] - strip2['box'][0][1]) < 50\
                angle_diff = calculate_angle_difference(strip1['contour'], strip2['contour'])
                if angle_diff < angle_diff_sensitivity:
                    paired_rices.append([strip1, strip2])
                break

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
    for i in range(len(rices)):
        strip1 = rices[i][0]
        for j in range(i + 1, len(rices)):
            strip2 = rices[j][0]
            angle_diff = calculate_angle_difference(strip1['contour'], strip2['contour'])
            if angle_diff < angle_diff_sensitivity and strip1['color_name'] != strip2['color_name']:
                robot_rices.append([rices[i], rices[j]])
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
