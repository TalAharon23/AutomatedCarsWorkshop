import cv2
from tkinter import *
from tkinter import Label, Button
from PIL import Image, ImageTk
from threading import Thread
from Movement_Handler import Movement_Handler
from Detection_Handler.Detection_controller import Detection_controller


class AutoPark:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Load the project image and resize it
        self.project_image = Image.open("Resources/logo_final.png")
        self.project_image = self.project_image.resize((320, 130), Image.ANTIALIAS)

        # Create a PhotoImage object from the resized image
        self.project_photo = ImageTk.PhotoImage(self.project_image)

        # Create a Label widget to display the image
        image_label = Label(window, image=self.project_photo)
        image_label.pack()

        # Create buttons below the image with a larger font size
        self.parking_button = Button(window, text="Parking", command=self.start_parking, width=30, bg="green",
                                     font=("Helvetica", 14))
        self.parking_button.pack()

        self.stop_button = Button(window, text="Stop", command=self.stop_function, width=30, bg="red",
                                  font=("Helvetica", 14))
        self.stop_button.pack()

        window.geometry("250x210")

        # Make the window non-resizable
        self.window.resizable(False, False)

        # Get the screen width
        screen_width = window.winfo_screenwidth()

        # Calculate the horizontal position for the top-right corner
        horizontal_position = screen_width - window.winfo_width()

        # Set the window position in the top-right corner
        window.geometry(f"+{horizontal_position - 250}+0")

        # Initialize Movement_Handler and Detection_controller
        self.detector = Detection_controller()
        self.image_logic = Movement_Handler()

        # Start the video scanning process in a thread
        Thread(target=self.start_video_scanning).start()

        # Initialize video capture for the UI
        self.video_capture = cv2.VideoCapture()
        self.update_ui()

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
        print("Starting car parking session!")
        self.image_logic.set_process_val(True)

        # Start the parking session in a new thread
        Thread(target=self.image_logic.start_car_parking_session).start()

    def stop_function(self):
        print("Stop button clicked")
        self.image_logic.set_process_val(False)

    def on_closing(self):
        self.video_capture.release()
        self.window.destroy()
