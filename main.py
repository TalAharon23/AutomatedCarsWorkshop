import tkinter as tk
import UI.main_screen as UI

def main():
    root = tk.Tk()
    app = UI.AutoPark(root, "AutoPark")
    root.mainloop()


if __name__ == '__main__':
    main()
