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


def Find_Car(frame, matrix, frameSize, car):
    global contours_list
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # cv2.rectangle(frame, (86,176), (86 + 2,176 + 2), (0), 2)
    # output_adapthresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 51, 0)
    # kernel = np.ones((3, 3), np.uint8)
    # output_erosion = cv2.erode(output_adapthresh, kernel, iterations = 12)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Reduce threshold to increase white noise
    # threshold1 = 150  # brightly lit
    # threshold2 = 330  # brightly lit
    threshold1 = 150    # afternoon
    threshold2 = 300    # afternoon
    edges = cv2.Canny(blurred, threshold1, threshold2)
    cv2.imshow("test", edges)
    # Find contours in the dilated image
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    pixelsPerMm = 2
    # rect = cv2.minAreaRect(contours[0])
    # box = cv2.boxPoints(rect)
    # box = np.int0(box)
    # cv2.drawContours(frame, [box], 0, (100, 100, 100), 2)

    # Filter the contours to find the red strips for the forward and black strips for the backward

    if contours != None:
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            # perimeter = cv2.arcLength(contour, False)
            approx = cv2.approxPolyDP(contour, perimeter, 3, True)
            x, y, w, h = cv2.boundingRect(contour)
            if len(approx) > 0 and len(approx) < 3: # and ((w > 25 and h < 25) or (h > 25 and w < 25)):
                # Check if the strip is red or black based on its average intensity

                box = cv2.minAreaRect(contour)
                box = cv2.boxPoints(box)
                # box = np.array(box, dtype="int")
                box = np.int0(box)
                # cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)

                (top_left, top_right, bottom_right, bottom_left) = box

                distance_a = distance.euclidean((top_left[0], top_left[1]), (top_right[0], top_right[1]))
                distance_b = distance.euclidean((top_left[0], top_left[1]), (bottom_left[0], bottom_left[1]))

                dimension_a = distance_a / pixelsPerMm
                dimension_b = distance_b / pixelsPerMm

                length = max(dimension_a, dimension_b)
                width = min(dimension_a, dimension_b)
                # if length < 1 or length > 70:
                #     continue
                # if width < 1 or width > 70:
                #     continue
                # if 900 > width * length or width * length > 2200:
                #     continue

                if length > 11 and length < 35 and width > 11 and width < 35 and width * length > 250 and width * length < 700:
                    rice = [box.astype("int")]
                    # Check class
                    strip_roi = gray[y:y+h, x:x+w]
                    avg_intensity = np.mean(strip_roi)
                    if avg_intensity > white_avg_intensity_bottom:
                        if check_contour_is_valid(rice):
                            for index in range(len(contours_list)):
                                if contours_list[index - 1]['color_name'] == 'white':
                                    pass
                                    # del contours_list[index - 1]
                            contours_list.append({'class': 'class1', 'box': rice, 'color': (255, 255, 255), 'width': width, 'color_name': 'white',
                                          'top_right': top_right, 'contour': contour})
                        # cv2.drawContours(frame, [box], 0, (255, 255, 255), 2)

                    elif avg_intensity < red_avg_intensity_top and avg_intensity > red_avg_intensity_bottom:
                        cv2.drawContours(frame, [box], 0, (255, 0, 0), 2)

                    else:
                        if check_contour_is_valid(rice):
                            for index in range(len(contours_list)):
                                if contours_list[index - 1]['color_name'] == 'black':
                                    pass
                                    # del contours_list[index - 1]

                            contours_list.append({'class': 'class3', 'box': rice, 'color': (0, 0, 0), 'width': width, 'color_name': 'black',
                                          'top_right': top_right, 'contour': contour})
                        # cv2.drawContours(frame, [box], 0, (0, 0, 0), 2)


                    # if len(contours_list) == 2:
                    #     break


        num_contours = len(contours_list)
        for i in range(num_contours):
            for j in range(i + 1, num_contours):
                angle_difference = calculate_angle_difference(contours_list[i], contours_list[j])
                if 0 <= angle_difference < 10 and contours_list[i]['color_name'] != contours_list[j]['color_name'] and calculate_distance(contours_list[i]['contour'], contours_list[j]['contour']) < 90:
                    cv2.drawContours(frame, contours_list[i]['box'], 0, contours_list[i]['color'], 2)
                    cv2.drawContours(frame, contours_list[j]['box'], 0, contours_list[j]['color'], 2)
                    print(calculate_actual_angle_difference(contours_list, calculate_curr_angle(contours_list[i]['contour'], contours_list[j]['contour'])))
                    car.set_direction_degrees(calculate_actual_angle_difference(contours_list, calculate_curr_angle(contours_list[i]['contour'], contours_list[j]['contour'])))
                    cX = cY = 0
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

                    car.set_position((cX, cY))
                    matrix[cY][cX] = Data_Structures.Val_dict.CAR
                    matrix[cY][cX + 1] = Data_Structures.Val_dict.CAR
                    matrix[cY + 1][cX] = Data_Structures.Val_dict.CAR
                    matrix[cY + 1][cX + 1] = Data_Structures.Val_dict.CAR

                        #     cv2.putText(frame, "{:}".format('Front'),
                        #                 (contours_list[i]['box'][0][0] + 10, contours_list[i]['box'][0][1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                        #                 (0, 0, 0), 1)
                        # else:
                        #     cv2.putText(frame, "{:}".format('Front'),
                        #                 (contours_list[j]['box'][0][0] + 10, contours_list[j]['box'][0][1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                        #                 (0, 0, 0), 1)



        while len(contours_list) > 2:
            del contours_list[0]



        # if angle_degrees < 0:
        #     angle_degrees += 360
        # car.set_position(get_white_strip_rice(robot_rices))
        # car.set_direction_degrees(int(round(angle_degrees)))
        # print(int(round(angle_degrees)))
        # cv2.putText(frame, "{:}".format('Front'),
        #             (boundries[0][0] - 10, boundries[2][0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.3,
        #             (255, 255, 255), 1)


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
        cX1, cY1, cX2, cY2,  = 0, 0

    distance = np.sqrt((cX1 - cX2)**2 + (cY1 - cY2)**2)
    return distance

def find_pairs(paired_rices, rices):
    pass
    # Find paired strips from the same color

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

def calculate_curr_angle(contour1, contour2):
    # Find the bounding rectangles of the contours
    rect1 = cv2.minAreaRect(contour1)
    rect2 = cv2.minAreaRect(contour2)
    # Get the angles of the bounding rectangles
    angle1 = rect1[2]
    angle2 = rect2[2]

    return (angle1 + angle2)/2


def find_robot(robot_rices, rices):
    pass
            # break

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

    for rice in robot_rices:
        if rice['color_name'] == 'white':
            strip_1 = rice
        elif rice['color_name'] == 'black':
            strip_2 = rice

    # print(strip_1['box'][0][0][0])
    # print(strip_2['box'][0][0][0])
    # print(strip_1['box'][0][0][1])
    # print(strip_2['box'][0][0][1])

    if strip_1['box'][0][0][0] < strip_2['box'][0][0][0] and strip_1['box'][0][0][1] < strip_2['box'][0][0][1]:
        # print(f"{curr_angle} + 270 = {curr_angle + 270}") #fix
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
        if cell[0] < 0 or cell [1] < 0:
            returnVal = False

    return returnVal
