import tkinter as tk
import cv2
from PIL import Image, ImageTk

root = tk.Tk()
root.geometry("1300x600")


def button_click():
    print("Button clicked")


parkingButton = tk.Button(root, text="Parking", command=button_click, height=5, width=15, bg="blue", fg="white",
                          font=("Arial", 30))
parkingButton.pack(pady=10)

stopButton = tk.Button(root, text="Stop", command=button_click, height=5, width=15, bg="blue", fg="white",
                       font=("Arial", 30))
stopButton.pack(pady=10)

canvas1 = tk.Canvas(root, width=320, height=240)
canvas1.pack(side=tk.LEFT)

canvas2 = tk.Canvas(root, width=320, height=240)
canvas2.pack(side=tk.RIGHT)

cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)  # use different capture devices for each canvas


def update_canvas(canvas, cap):
    ret, frame = cap.read()
    if ret:
        # convert the frame to a PIL Image object
        image = Image.fromarray(frame)

        # convert the PIL Image object to a PhotoImage object that can be displayed on a Canvas
        photo = ImageTk.PhotoImage(image)

        # display the PhotoImage on the Canvas
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)

        # keep a reference to the PhotoImage to prevent it from being garbage collected
        canvas.photo = photo

    # schedule the next update after 10 milliseconds
    root.after(10, update_canvas, canvas, cap)


# start the update loop for both canvases
update_canvas(canvas1, cap1)
update_canvas(canvas2, cap2)

root.mainloop()  # start the main event loop
