import cv2
import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
from threading import Thread
from Movement_Handler import Movement_Handler
from Detection_Handler.Detection_controller import Detection_controller


class CarApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Create header label
        self.header_label = Label(window, text="Car Project", font=("Helvetica", 16))
        self.header_label.pack()

        # Create a frame for image display
        self.image_frame = tk.Frame(window)
        self.image_frame.pack()

        # Create labels for images
        self.image_labels = []
        for _ in range(4):
            label = Label(self.image_frame)
            label.pack(side="left")
            self.image_labels.append(label)

        # Create buttons
        self.parking_button = Button(window, text="Parking", command=self.start_parking)
        self.parking_button.pack()

        self.stop_button = Button(window, text="Stop", command=self.stop_function)
        self.stop_button.pack()

        # Initialize Movement_Handler and Detection_controller
        self.detector = Detection_controller()
        self.image_logic = Movement_Handler()

        # Start the video scanning process in a thread
        Thread(target=self.start_video_scanning).start()

        # Initialize video capture for the UI
        self.video_capture = cv2.VideoCapture()
        self.update_ui()
        # self.parking_session_active = False

    def start_video_scanning(self):
        a = 2
        self.detector.scan_video(self.image_logic.robot, self.image_logic.parking_slots)

    def update_ui(self):
        ret, frame = self.video_capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            for label in self.image_labels:
                label.config(image=photo)
                label.image = photo

        self.window.after(10, self.update_ui)

    def start_parking(self):
        self.image_logic.set_process_val(True)

        # Start the parking session in a new thread
        Thread(target=self.image_logic.start_car_parking_session).start()

    def stop_function(self):
        # Function to be called when the "Stop" button is clicked
        print("Stop button clicked")

        # Add your stop logic here if needed
        # Set the flag to stop the parking session
        # self.parking_session_active = False
        self.image_logic.set_process_val(False)

    def on_closing(self):
        self.video_capture.release()
        self.window.destroy()
