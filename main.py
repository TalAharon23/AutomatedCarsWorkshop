import cv2
import glob
import os
import numpy as np
import threading


from ESP32CAM_Car.MovementAPI import move
import Detection_Handler.Detection_controller as logic


def main():
    image_logic = logic.Detection_controller()
    # Create a thread for the video scanning process
    video_thread = threading.Thread(target=image_logic.scan_video)
    video_thread.start()
    # Create a thread for the GUI
    gui_thread = threading.Thread(target=image_logic.create_buttons)
    gui_thread.start()



if __name__ == '__main__':
    main()
