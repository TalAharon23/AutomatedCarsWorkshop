import cv2
import glob
import os
import numpy as np

import Detection_Handler.Line_Handler as ln_h
import Detection_Handler.Car_Handler
import Detection_Handler.Parking_Handler
import Detection_Handler.Boundaries_Handler as bd_h

frameSize = (700, 500)
val_dict = {
    "Border": 1,
    "Line": 2,
    "Parking_slot": 3,
    "Robot": 4
}

def main():
    ## Use this line for saved video:
    # src_video = cv2.VideoCapture('Resources/Amir_Test/sample.mp4')

    # Real time video from the upper camera
    src_video = cv2.VideoCapture(0)
    matrix = np.zeros(frameSize)
    mask_line = 'Line'
    mask_border = 'Border'


    # Processed video from our models (output video in the end of the app)
    out_video = cv2.VideoWriter('Resources/Amir_Test/output_video.avi', cv2.VideoWriter_fourcc(*'DIVX'), 24, frameSize)
    while (src_video.isOpened()):
        # Capture frame-by-frame
        ret, frame = src_video.read()
        if (type(frame) == type(None)):
            pass
        else:
            template_data = bd_h.Create_Template(frame, matrix, frameSize, val_dict)
            if template_data[0] == True:
                matrix = template_data[1]
                frame = cv2.resize(frame, frameSize, fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
                processed_frame = ln_h.Find_Lines(frame, matrix, frameSize, mask_line, val_dict)[1]
                # processed_frame = ln_h.Find_Car(frame, matrix, frameSize)[1]             # Sholmait
                # processed_frame = ln_h.Find_Lines(frame, matrix, frameSize, mask_border, val_dict)[1]      # Shriki
                # processed_frame = ln_h.Find_Parking_Lots(frame, matrix, frameSize)[1]    # Jacob
                # Display the resulting frame
            cv2.imshow('Frame', processed_frame)

            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
            out_video.write(processed_frame)

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
