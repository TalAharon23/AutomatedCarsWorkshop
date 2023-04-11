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


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# main class
class Detection_controller(BaseClass, metaclass=Singleton):
    # Use this line for saved video:
    # src_video = cv2.VideoCapture('Resources/Amir_Test/sample.mp4')

    # Real time video from the phone camera
    url = "http://192.168.1.215:8080/video"
    src_video = cv2.VideoCapture(url)
    matrix = np.zeros(frameSize)
    mask_line = 'Path'
    mask_border = 'Border'
    counter = 0
    num_of_frame_for_stabiliztion = 0
    # Processed video from our models (output video in the end of the app)
    out_video = cv2.VideoWriter('Resources/Amir_Test/output_video.avi', cv2.VideoWriter_fourcc(*'DIVX'), 24, frameSize)

    def scan_video(self):
        while (src_video.isOpened()):
            # Capture frame-by-frame
            ret, frame = src_video.read()
            if type(frame) == type(None):
                pass
            elif counter % 3 == 0:
                self.get_avg_matix()
                out_video.write(processed_frame)
            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            counter += 1
            # Assuming it failed to read only the last frame - video end
            if not ret:
                break

            q = cv2.waitKey(1)
            if q == ord("q"):
                break
        out_video.release()

        # release the src_video capture object
        src_video.release()
        # Closes all the windows currently opened.
        cv2.destroyAllWindows()

    def get_avg_matix(self, fram_array):
        template_data = True, matrix  # .Create_Template(frame, matrix, frameSize, val_dict)
        if template_data[0] == True:
            matrix = template_data[1]

        frame = cv2.resize(frame, frameSize, fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
        processed_frame = ln_h.Find_Lines(frame, matrix, frameSize, mask_line, val_dict)[1]  # Find lines
        processed_frame = ln_h.Find_Lines(frame, matrix, frameSize, mask_border, val_dict)[1]  # Find borders
        processed_frame, matrix = park_h.Find_Parking(frame, matrix, frameSize)  # Find parking spot
        # processed_frame = car_h.Find_Car(frame, matrix, frameSize)[1]             # Sholmait
        # Display the resulting frame
        cv2.imshow('Frame', processed_frame)

        return processed_frame