import cv2
import glob
import os
import numpy as np

from ESP32CAM_Car.MovementAPI import move
import Detection_Handler.Detection_controller as logic


def main():
    image_logic = logic.Detection_controller()
    image_logic.scan_video()


if __name__ == '__main__':
    main()
