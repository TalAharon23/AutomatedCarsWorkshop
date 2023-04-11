import cv2
import glob
import os
import numpy as np

import Detection_Handler.Detection_controller as logic


def main():
    image_logic = logic.Detection_controller()
    image_logic.scan_video()


if __name__ == '__main__':
    main()
