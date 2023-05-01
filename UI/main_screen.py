# import tkinter as tk
# import cv2
# from PIL import Image, ImageTk
#
# root = tk.Tk()
# root.geometry("1300x500")
#
#
# def parkingButton_click():
#     print("Parking Button clicked")
#
# def stopButton_click():
#     print("Stop Button clicked")
#
#
# parkingButton = tk.Button(root, text="Parking", command=parkingButton_click, height=4, width=10, bg="blue", fg="white", font=("Arial", 30))
# parkingButton.pack(pady=10)
#
# stopButton = tk.Button(root, text="Stop", command=stopButton_click, height=4, width=10, bg="blue", fg="white", font=("Arial", 30))
# stopButton.pack(pady=10)
#
# canvas1 = tk.Canvas(root, width=320, height=240)
# canvas1.place(x=0, y=0, anchor="nw")
# canvas1.config(width=500, height=457)
#
# canvas2 = tk.Canvas(root, width=320, height=240)
# canvas2.place(x=0, y=0, anchor="ne")
# canvas2.config(width=500, height=457)
#
# cap1 = cv2.VideoCapture(0)
# cap2 = cv2.VideoCapture(1)  # use different capture devices for each canvas
#
#
# def update_canvas(canvas, cap):
#     ret, frame = cap.read()
#     if ret:
#         # convert the frame to a PIL Image object
#         image = Image.fromarray(frame)
#
#         # convert the PIL Image object to a PhotoImage object that can be displayed on a Canvas
#         photo = ImageTk.PhotoImage(image)
#
#         # display the PhotoImage on the Canvas
#         canvas.create_image(0, 0, anchor=tk.NW, image=photo)
#
#         # keep a reference to the PhotoImage to prevent it from being garbage collected
#         canvas.photo = photo
#
#     # schedule the next update after 10 milliseconds
#     root.after(10, update_canvas, canvas, cap)
#
#
# # start the update loop for both canvases
# update_canvas(canvas1, cap1)
# update_canvas(canvas2, cap2)
#
# button_frame = tk.Frame(root)
# button_frame.pack(pady=10)
#
# button1 = tk.Button(button_frame, text="Parking", bg="green", width=10, height=2)
# button1.pack(side=tk.LEFT, padx=10)
#
# button2 = tk.Button(button_frame, text="Stop", bg="red", width=10, height=2)
# button2.pack(side=tk.LEFT, padx=10)
#
# root.geometry("1300x600")
# button1.place(x=100, y=300)
# button2.place(x=300, y=300)
#
#
#
# root.mainloop()  # start the main event loop
#
#
