import cv2
import numpy as np
import threading

import Data_Structures
import Detection_Handler.Line_Handler as ln_h
import Detection_Handler.Car_Handler as car_h
import Detection_Handler.Parking_Handler as park_h
import Detection_Handler.Boundaries_Handler as bd_h

# frameSize = (900, 900)
frameSize = (600, 650) # For using laptop only
val_dict = {
    "Border": 1,
    "Path": 2,
    "Parking_slot": 3,
    "Robot": 4
}
mask_line = 'Path'
mask_border = 'Border'
url = "http://10.100.102.33:8080/video"
# url = "http://192.168.245.4:8s080/video"


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


matrix  = np.zeros(frameSize)
videoIsLive = True
processed_frame = None
DS_lock = threading.Lock()
box = None


# main class
class Detection_controller(metaclass=Singleton):

    def __init__(self):
        self.num_of_frame_for_stabiliztion          = 0
        self.counter                                = 0
        self.src_video                              = cv2.VideoCapture(url)
        self.out_video                              = cv2.VideoWriter('Resources/Amir_Test/output_video.avi',
                                                                      cv2.VideoWriter_fourcc(*'DIVX'), 12,frameSize)
        self.matrix                                 = np.zeros(frameSize)
        self.frame_array                            = []
        self.flag                                   = True
        self.framenum                               = 0
        # self.parking_slots                          = Data_Structures.Parking_Slots()

    def scan_video(self, car, parking_slots):
        while (self.src_video.isOpened()):
            DS_lock.acquire()
            videoIsLive = True
            DS_lock.release()
            # Capture frame-by-frame
            ret, frame = self.src_video.read()
            # Assuming it failed to read only the last frame - video end
            if not ret:
                DS_lock.acquire()
                videoIsLive = False
                DS_lock.release()
                break
            if self.counter == 6:
                # self.matrix = bd_h.Create_Template(self.frame_array)
                pass
            elif self.counter < 6:
                self.frame_array.append(self.scan_frame(frame, car, parking_slots))
            elif self.counter % 5 == 0:
                DS_lock.acquire()
                processed_frame = self.scan_frame(frame, car, parking_slots)
                self.out_video.write(processed_frame)
                DS_lock.release()
            self.counter += 1
            q = cv2.waitKey(1)
            if q == ord("q"):
                break
        DS_lock.acquire()
        videoIsLive = False
        DS_lock.release()

        DS_lock.acquire()
        self.out_video.release()
        # release the src_video capture object
        self.src_video.release()
        DS_lock.release()
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

    def scan_frame(self, frame, car, parking_slots):
        global matrix
        global box

        frame = cv2.resize(frame, frameSize, fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
        origin_frame = frame.copy()
        # processed_frame = ln_h.Find_Lines(frame, matrix, frameSize, mask_line, val_dict)[1q]  # Find path
        # processed_frame = ln_h.Find_Lines(frame, matrix, frameSize, mask_border, val_dict)[1]  # Find borders
        if len(parking_slots.get_parking_slots()) < 2:
            box, matrix = park_h.Find_Parking_Slots(frame, matrix, frameSize, val_dict,
                                                                parking_slots)  # Find parking spot
        else:
            for cnt in parking_slots.get_parking_slots_contours():
                # epsilon = 0.01 * cv2.arcLength(cnt, True)

                perimeter = cv2.arcLength(cnt, True)
                # perimeter = cv2.arcLength(contour, False)
                approx = cv2.approxPolyDP(cnt, perimeter, 3, True)
                # approx = cv2.approxPolyDP(cnt, epsilon, True)

                box = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(box)
                # box = np.array(box, dtype="int")
                box = np.int0(box)

        processed_frame = car_h.Find_Car(frame, matrix, frameSize, car)[1]

        if box is not None:
            cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)


        matrix_scaled = cv2.normalize(matrix, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        cv2.imwrite('matrix_img.jpg', matrix_scaled)
        cv2.rotate(matrix_scaled, cv2.ROTATE_90_CLOCKWISE)
        cv2.imshow('Matrix image', matrix_scaled)
        # Display the resulting frame
        h_concat = np.hstack((origin_frame, processed_frame))
        q = cv2.waitKey(1)
        if q == ord("q"):
            cv2.destroyAllWindows()

        # Display the concatenated frame
        cv2.imshow('Autonomous Car', h_concat)
        return processed_frame

    @staticmethod
    def get_processed_frame():
        pass

    @staticmethod
    def isVideoOnLive():
        DS_lock.acquire()
        temp_status = videoIsLive
        DS_lock.release()
        return temp_status

    @staticmethod
    def get_matrix():
        DS_lock.acquire()
        temp_matrix = matrix.copy()
        DS_lock.release()
        return temp_matrix

    @staticmethod
    def set_matrix(new_matrix):
        global matrix
        DS_lock.acquire()
        matrix = new_matrix
        DS_lock.release()

    def reset_Matrix(self):
        global matrix
        DS_lock.acquire()
        matrix = np.zeros(frameSize)
        DS_lock.release()

    @staticmethod
    def get_matrix_size():
        return frameSize
