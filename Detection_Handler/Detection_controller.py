import cv2
import numpy as np

import Data_Structures
import Detection_Handler.Line_Handler as ln_h
import Detection_Handler.Car_Handler as car_h
import Detection_Handler.Parking_Handler as park_h
import Detection_Handler.Boundaries_Handler as bd_h

#frameSize = (900, 900)
frameSize = (650, 650) # For using laptop only
val_dict = {
    "Border": 1,
    "Path": 2,
    "Parking_slot": 3,
    "Robot": 4
}
mask_line = 'Path'
mask_border = 'Border'
url = "http://192.162.3.194:8080/video"


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# main class
class Detection_controller(metaclass=Singleton):

    def __init__(self):
        self.num_of_frame_for_stabiliztion          = 0
        self.counter                                = 0
        self.src_video                              = cv2.VideoCapture(url)
        self.out_video                              = cv2.VideoWriter('Resources/Amir_Test/output_video.avi',
                                                                      cv2.VideoWriter_fourcc(*'DIVX'), 24,frameSize)
        self.matrix                                 = np.zeros(frameSize)
        self.frame_array                            = []
        self.flag                                   = True
        self.framenum                               = 0
        self.parking_slots                          = Data_Structures.Parking_Slots()


    def scan_video(self, car):
        while (self.src_video.isOpened()):
            # Capture frame-by-frame
            ret, frame = self.src_video.read()
            # Assuming it failed to read only the last frame - video end
            if not ret:
                break
            if self.counter == 6:
                # self.matrix = bd_h.Create_Template(self.frame_array)
                pass
            elif self.counter < 6:
                self.frame_array.append(self.scan_frame(frame, car))
            elif self.counter % 3 == 0:
                processed_frame = self.scan_frame(frame, car)[0]
                self.out_video.write(processed_frame)
            self.counter += 1
            q = cv2.waitKey(1)
            if q == ord("q"):
                break

        self.out_video.release()
        # release the src_video capture object
        self.src_video.release()
        # Closes all the windows currently opened.
        cv2.destroyAllWindows()

    def print_matrix(self, matrix):
        """for rows in range(matrix.shape[0]):
            for cols in range(matrix.shape[1]):
                print(str(matrix[rows][cols]) + " ")
            print()"""
        np.set_printoptions(threshold=np.inf)

        # print the matrix
        # print(matrix)
        matrix_scaled = cv2.normalize(matrix, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        cv2.imwrite("matrix_image" + str(self.framenum) + ".jpg", matrix_scaled)

    def scan_frame(self, frame, car):
        frame = cv2.resize(frame, frameSize, fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
        origin_frame = frame.copy()
        # processed_frame = ln_h.Find_Lines(frame, self.matrix, frameSize, mask_line, val_dict)[1q]  # Find path
        processed_frame = ln_h.Find_Lines(frame, self.matrix, frameSize, mask_border, val_dict)[1]  # Find borders
        processed_frame, matrix = park_h.Find_Parking_Slots(frame, self.matrix, frameSize, val_dict, self.parking_slots)  # Find parking spot
        processed_frame = car_h.Find_Car(frame, self.matrix, frameSize, car)[1]

        matrix_scaled = cv2.normalize(self.matrix, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        cv2.imwrite('color_img.jpg', matrix_scaled)
        cv2.rotate(matrix_scaled, cv2.ROTATE_90_CLOCKWISE)
        cv2.imshow('Color image', matrix_scaled)
        # Display the resulting frame
        h_concat = np.hstack((origin_frame, processed_frame))

        # Display the concatenated frame
        cv2.imshow('Autonomous Car', h_concat)
        return processed_frame, self.matrix

    def get_matrix(self):
        return self.matrix

    def get_matrix_size(self):
        return frameSize