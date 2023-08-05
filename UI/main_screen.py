import tkinter as tk
from ESP32CAM_Car.MovementAPI import move


def create_buttons():
    def on_parking_click():
        print("Start parking!")
        move("parking")

    def on_stop_click():
        print("Stopping car!")
        move("stop")

    root = tk.Tk()
    # root.geometry("30x500+83+103")
    root.wm_attributes("-topmost", 1)
    root.title("Controller")

    # Create Button 1 with text "Parking" and bind it to the on_buttonParking_click() function
    buttonParking = tk.Button(root, text="Parking", command=on_parking_click, width=15, height=3, bg="green",
                              font=("Arial", 16))
    buttonParking.pack()

    # Create Button 2 with text "Stop" and bind it to the on_buttonStop_click() function
    buttonStop = tk.Button(root, text="Stop", command=on_stop_click, width=15, height=3, bg="red",
                           font=("Arial", 16))
    buttonStop.pack()

    # Set the size of the root window to fit the buttons
    root.geometry("{}x{}".format(max(buttonParking.winfo_reqwidth(), buttonStop.winfo_reqwidth()),
                                 buttonParking.winfo_reqheight() + buttonStop.winfo_reqheight()))

    # Start the tkinter event loop
    root.mainloop()