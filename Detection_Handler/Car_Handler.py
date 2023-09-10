import cv2
import numpy as np
from scipy.spatial import distance
import Data_Structures
import copy

upside_left_corner = (0, 0)
white_avg_intensity_bottom = red_avg_intensity_top = 120
red_avg_intensity_bottom = 120
angle_diff_sensitivity = 15
pairs_distance_sensitivity = 15
contours_list = []
# degrees_symbol = "\u00b0"
degrees_symbol = "°"


def Find_Car(frame, matrix, car):
    global contours_list
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Reduce threshold to increase white noise
    # threshold1 = 150  # brightly lit
    # threshold2 = 330  # brightly lit
    threshold1 = 150  # afternoon
    threshold2 = 300  # afternoon
    edges = cv2.Canny(blurred, threshold1, threshold2)
    cv2.imshow("test", edges)

    # Find contours in the dilated image
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    pixelsPerMm = 2

    # Filter the contours to find the red strips for the forward and black strips for the backward
    if contours is not None:
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, perimeter, 3, True)
            x, y, w, h = cv2.boundingRect(contour)
            if 0 < len(approx) < 3:

                # Check if the strip is red or black based on its average intensity
                box = cv2.minAreaRect(contour)
                box = cv2.boxPoints(box)
                box = np.int0(box)

                (top_left, top_right, bottom_right, bottom_left) = box

                distance_a = distance.euclidean((top_left[0], top_left[1]), (top_right[0], top_right[1]))
                distance_b = distance.euclidean((top_left[0], top_left[1]), (bottom_left[0], bottom_left[1]))

                dimension_a = distance_a / pixelsPerMm
                dimension_b = distance_b / pixelsPerMm

                length = max(dimension_a, dimension_b)
                width = min(dimension_a, dimension_b)

                if 11 < length < 35 and 11 < width < 35 and 250 < width * length < 700:
                    rice = [box.astype("int")]
                    strip_roi = gray[y:y + h, x:x + w]
                    avg_intensity = np.mean(strip_roi)
                    if avg_intensity > white_avg_intensity_bottom:
                        if check_contour_is_valid(rice):
                            for index in range(len(contours_list)):
                                if contours_list[index - 1]['color_name'] == 'white':
                                    pass
                            contours_list.append(
                                {'class': 'class1', 'box': rice, 'color': Data_Structures.white, 'width': width,
                                 'color_name': 'white',
                                 'top_right': top_right, 'contour': contour})

                    elif red_avg_intensity_top > avg_intensity > red_avg_intensity_bottom:
                        cv2.drawContours(frame, [box], 0, Data_Structures.red, 2)

                    else:
                        if check_contour_is_valid(rice):
                            for index in range(len(contours_list)):
                                if contours_list[index - 1]['color_name'] == 'black':
                                    pass

                            contours_list.append({'class': 'class3', 'box': rice, 'color': Data_Structures.black,
                                                  'width': width,
                                                  'color_name': 'black',
                                                  'top_right': top_right, 'contour': contour})

        num_contours = len(contours_list)
        for i in range(num_contours):
            for j in range(i + 1, num_contours):
                angle_difference = calculate_angle_difference(contours_list[i], contours_list[j])
                if 0 <= angle_difference < 10 and contours_list[i]['color_name'] != contours_list[j][
                    'color_name'] and calculate_distance(contours_list[i]['contour'], contours_list[j]['contour']) < 90:
                    cv2.drawContours(frame, contours_list[i]['box'], 0, contours_list[i]['color'], 2)
                    cv2.drawContours(frame, contours_list[j]['box'], 0, contours_list[j]['color'], 2)
                    # print(calculate_actual_angle_difference([contours_list[i], contours_list[j]],
                    #                                         calculate_curr_angle_before_optimization(contours_list[i]['contour'],
                    #                                                              contours_list[j]['contour'])))
                    car.set_direction_degrees(calculate_actual_angle_difference([contours_list[i],
                                                                                 contours_list[j]],
                                                                                calculate_curr_angle_before_optimization(
                                                                                    contours_list[i]['contour'],
                                                                                    contours_list[j]['contour'])))

                    if contours_list[i]['color_name'] == 'white':
                        M1 = cv2.moments(contours_list[i]['contour'])
                        M2 = cv2.moments(contours_list[j]['contour'])
                    else:
                        M1 = cv2.moments(contours_list[j]['contour'])
                        M2 = cv2.moments(contours_list[i]['contour'])

                    if M1["m00"] != 0 and M2["m00"] != 0:
                        cX1 = int(M1["m10"] / M1["m00"])
                        cY1 = int(M1["m01"] / M1["m00"])
                        cX2 = int(M2["m10"] / M2["m00"])
                        cY2 = int(M2["m01"] / M2["m00"])

                        cX = int(round((cX1 + cX2) / 2))
                        cY = int(round((cY1 + cY2) / 2))
                    else:
                        cX, cY = 0, 0

                    car.set_position(Data_Structures.Cell(cX, cY))
                    matrix[cY][cX] = Data_Structures.Val_dict.CAR
                    matrix[cY][cX + 1] = Data_Structures.Val_dict.CAR
                    matrix[cY + 1][cX] = Data_Structures.Val_dict.CAR
                    matrix[cY + 1][cX + 1] = Data_Structures.Val_dict.CAR

                    # Print the robot direction in degrees
                    cv2.putText(frame, "{:}".format(f"{int(car.get_direction_degrees())} d"),
                                (car.get_position().X() + 40, car.get_position().Y() + 10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.45,
                                Data_Structures.black, 1, cv2.LINE_AA)

        while len(contours_list) > 2:
            del contours_list[0]

    return matrix, frame


def calculate_distance(contour1, contour2):
    # Calculate the Euclidean distance between the centroids of the contours
    M1 = cv2.moments(contour1)
    M2 = cv2.moments(contour2)

    if M1["m00"] != 0 and M2["m00"] != 0:
        cX1 = int(M1["m10"] / M1["m00"])
        cY1 = int(M1["m01"] / M1["m00"])
        cX2 = int(M2["m10"] / M2["m00"])
        cY2 = int(M2["m01"] / M2["m00"])
    else:
        cX1, cY1, cX2, cY2, = 0, 0

    distance_res = np.sqrt((cX1 - cX2) ** 2 + (cY1 - cY2) ** 2)
    
    return distance_res


def calculate_angle_difference(contour1, contour2):
    # Find the bounding rectangles of the contours
    rect1 = cv2.minAreaRect(contour1['contour'])
    rect2 = cv2.minAreaRect(contour2['contour'])

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


def calculate_curr_angle_before_optimization(contour1, contour2):
    # Find the bounding rectangles of the contours
    rect1 = cv2.minAreaRect(contour1)
    rect2 = cv2.minAreaRect(contour2)
    # Get the angles of the bounding rectangles
    angle1 = rect1[2]
    angle2 = rect2[2]

    return (angle1 + angle2) / 2


def find_center(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2
    return (center_x, center_y)


def calculate_actual_angle_difference(robot_rices, curr_angle):
    strip_1 = None
    strip_2 = None

    for rice in robot_rices:
        if rice['color_name'] == 'white':
            strip_1 = rice
        elif rice['color_name'] == 'black':
            strip_2 = rice

    if strip_1['box'][0][0][0] < strip_2['box'][0][0][0] and strip_1['box'][0][0][1] < strip_2['box'][0][0][1]:
        return curr_angle + 270
    elif strip_1['box'][0][0][0] < strip_2['box'][0][0][0] and strip_1['box'][0][0][1] > strip_2['box'][0][0][1]:
        return curr_angle + 180
    elif strip_1['box'][0][0][0] > strip_2['box'][0][0][0] and strip_1['box'][0][0][1] < strip_2['box'][0][0][1]:
        return curr_angle + 0
    else:
        return curr_angle + 90


def check_contour_is_valid(box):
    returnVal = True
    for cell in box[0]:
        if cell[0] < 0 or cell[1] < 0:
            returnVal = False

    return returnVal
