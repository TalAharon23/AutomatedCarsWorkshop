import cv2
import numpy as np

url = "http://192.168.1.201:8080/video"
cp = cv2.VideoCapture(url)

while True:
    ret, frame = cp.read()
    if ret:
        # resize the frame to half its original size
        new_size = (int(frame.shape[1] / 2), int(frame.shape[0] / 2))
        frame = cv2.resize(frame, new_size)

        cv2.imshow("Frame", frame)
    q = cv2.waitKey(1)
    if q == ord("q"):
        break

cv2.destroyAllWindows()
