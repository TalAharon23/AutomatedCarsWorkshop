import tkinter as tk

def create_buttons(self):
    def on_button1_click():
        print("Button 1 clicked!")

    def on_button2_click():
        print("Button 2 clicked!")

    root = tk.Tk()
    root.geometry("30x500+83+103")
    root.wm_attributes("-topmost", 1)

    # Create Button 1 with text "Button 1" and bind it to the on_button1_click() function
    button1 = tk.Button(root, text="Parking", command=on_button1_click, width=45, height=3, bg="green",
                        font=("Arial", 16))
    button1.pack()

    # Create Button 2 with text "Button 2" and bind it to the on_button2_click() function
    button2 = tk.Button(root, text="Stop", command=on_button2_click, width=45, height=3, bg="red",
                        font=("Arial", 16))
    button2.pack()

    # Start the tkinter event loop
    root.mainloop()