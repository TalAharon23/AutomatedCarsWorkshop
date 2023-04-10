import cv2
import glob
import os
import numpy as np

import Detection_Handler.Line_Handler as ln_h
import Detection_Handler.Car_Handler as car_h
import Detection_Handler.Parking_Handler
import Detection_Handler.Boundaries_Handler

frameSize = (700, 500)

def main():
    ## Use this line for saved video:
    # src_video = cv2.VideoCapture('Resources/Amir_Test/sample.mp4')

    # Real time video from the upper camera
    src_video = cv2.VideoCapture(0)
    matrix = np.zeros(frameSize)

    # Processed video from our models (output video in the end of the app)
    out_video = cv2.VideoWriter('Resources/Amir_Test/output_video.avi', cv2.VideoWriter_fourcc(*'DIVX'), 24, frameSize)
    while (src_video.isOpened()):
        # Capture frame-by-frame
        ret, frame = src_video.read()
        if (type(frame) == type(None)):
            pass
        else:
            frame = cv2.resize(frame, frameSize, fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
            # processed_data = ln_h.Find_Lines(frame, matrix, frameSize)
            processed_data = car_h.Find_Car(frame, matrix, frameSize)           # Sholmait
            # processed_frame = ln_h.Find_Boundaries(frame, matrix, frameSize)[1]      # Shriki
            # processed_frame = ln_h.Find_Parking_Lots(frame, matrix, frameSize)[1]    # Jacob
            # Display the resulting frame
            cv2.imshow('Frame', processed_data[1])

            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            out_video.write(processed_data[1])

        # Assuming it failed to read only the last frame - video end
        if ret == False:
            break

    out_video.release()

    # release the src_video capture object
    src_video.release()
    # Closes all the windows currently opened.
    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()

