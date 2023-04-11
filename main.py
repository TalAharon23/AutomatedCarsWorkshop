import cv2
import glob
import os
import numpy as np

import Detection_Handler.Line_Handler as ln_h
import Detection_Handler.Car_Handler as car_h
import Detection_Handler.Parking_Handler as park_h
import Detection_Handler.Boundaries_Handler as bd_h
import Detection_Handler.Detection_controller


def main():
    image_logic = Detection_controller()


if __name__ == '__main__':
    main()
