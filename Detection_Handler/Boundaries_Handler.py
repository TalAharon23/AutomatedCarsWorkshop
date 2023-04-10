import cv2
import numpy as np
import Detection_Handler.Line_Handler as ln_h

num_of_frames = 6
res_index = 0
threshold = 0.7


def Create_Template(frame, matrix, frameSize, val_dict):
    # make averege
    res = False
    Create_Template.counter += 1
    Create_Template.data[Create_Template.counter] = ln_h.Find_Lines(frame, matrix, frameSize,
                                                                    'Path', val_dict)[0]

    if Create_Template.counter >= num_of_frames:
        for index in range(Create_Template.counter):
            Create_Template.data[res_index] += Create_Template.data[index]
        get_final_matrix(matrix, Create_Template.counter, val_dict)
        Create_Template.counter = 0
        res = True

    return res, matrix


def get_final_matrix(matrix, counter, val_dict):
    matrix = matrix / counter
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > threshold:
                matrix[i][j] = 1
            else:
                matrix[i][j] = 0
