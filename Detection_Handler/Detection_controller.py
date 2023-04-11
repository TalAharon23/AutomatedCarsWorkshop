import cv2
import glob
import os
import numpy as np

import Detection_Handler.Line_Handler as ln_h
import Detection_Handler.Car_Handler as car_h
import Detection_Handler.Parking_Handler as park_h
import Detection_Handler.Boundaries_Handler as bd_h

frameSize = (700, 500)
val_dict = {
    "Border": 1,
    "Path": 2,
    "Parking_slot": 3,
    "Robot": 4
}
mask_line = 'Path'
mask_border = 'Border'
url = "http://192.168.1.250:8080/video"


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# main class
class Detection_controller(metaclass=Singleton):
    # Use this line for saved video:
    # src_video = cv2.VideoCapture('Resources/Amir_Test/sample.mp4')
    # Real time video from the phone camera
    # src_video = None
    # matrix = None
    # num_of_frame_for_stabiliztion = 0
    # Processed video from our models (output video in the end of the app)
    # out_video = None

    def __init__(self):
        self.num_of_frame_for_stabiliztion = 0
        self.counter = 0
        self.src_video = cv2.VideoCapture(url)
        self.out_video = cv2.VideoWriter('Resources/Amir_Test/output_video.avi', cv2.VideoWriter_fourcc(*'DIVX'), 24,
                                    frameSize)
        self.matrix = np.zeros(frameSize)
        self.frame_array = []

    def scan_video(self):
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
                self.frame_array.append(self.scan_frame(frame))
            elif self.counter % 3 == 0:
                processed_frame = self.scan_frame(frame)[0]
                self.out_video.write(processed_frame)

            self.counter += 1
            q = cv2.waitKey(1)
            if q == ord("q"):
                break
        out_video.release()

        # release the src_video capture object
        src_video.release()
        # Closes all the windows currently opened.
        cv2.destroyAllWindows()

    def scan_frame(self, frame):
        frame = cv2.resize(frame, frameSize, fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
        origin_frame = frame.copy()
        processed_frame = ln_h.Find_Lines(frame, self.matrix, frameSize, mask_line, val_dict)[1]  # Find lines
        processed_frame = ln_h.Find_Lines(frame, self.matrix, frameSize, mask_border, val_dict)[1]  # Find borders
        processed_frame, matrix = park_h.Find_Parking(frame, self.matrix, frameSize)  # Find parking spot
        # processed_frame = car_h.Find_Car(frame, matrix, frameSize)[1]

        # Display the resulting frame
        h_concat = np.hstack((origin_frame, processed_frame))

        # Display the concatenated frame
        cv2.imshow('Autonomous Car', h_concat)
        return processed_frame, matrix