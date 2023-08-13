import cv2
import glob
import os
import numpy as np
import threading

from ESP32CAM_Car.MovementAPI import move
import Detection_Handler.Detection_controller as logic
import UI.main_screen as UI
import Movement_Handler

# Will be deleted and moved into Movement_Handler
import Data_Structures as DS



def main():
    image_logic = Movement_Handler.Movement_Handler()
    # Create a thread for the video scanning process
    image_logic.start_car_parking_session()
    # video_thread = threading.Thread(target=image_logic.start_car_parking_session, args=[])
    # video_thread.start()
    # Create a thread for the GUI
    # gui_thread = threading.Thread(target=UI.create_buttons)
    # gui_thread.start()


if __name__ == '__main__':
    main()
