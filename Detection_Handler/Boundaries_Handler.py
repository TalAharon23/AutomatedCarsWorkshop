import cv2
import numpy as np
import Detection_Handler.Line_Handler as ln_h
import Data_Structures

num_of_frames = 6
res_index = 0
threshold = 0.7


def Create_Template(frame_array):
    # make averege
    """
    res = False
    counter += 1
    fram_array[Create_Template.counter] = ln_h.Find_Lines(frame, matrix, frameSize, 'Path')[0]
    if counter >= num_of_frames:
        for index in range(Create_Template.counter):
            fram_array[res_index] += fram_array[index]
        get_final_matrix(matrix, counter)
        counter = 0
        res = True"""

    return # res, matrix


def get_final_matrix(matrix, counter):
    matrix = matrix / counter
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > threshold:
                matrix[i][j] = 1
            else:
                matrix[i][j] = 0
