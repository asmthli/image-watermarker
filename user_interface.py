import tkinter as tk


class UI:
    BACKGROUND_COLOUR = "grey"

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Image Watermarker")
        self.window.config(background=UI.BACKGROUND_COLOUR)

        self.image = Image()
        self.menu = Menu()

    def start_event_loop(self):
        self.window.mainloop()


class Menu:
    def __init__(self):
        self.canvas = tk.Canvas(width=800, height=100, background="indigo")
        self.canvas.grid(row=1, column=0)


class Image:
    def __init__(self):
        self.canvas = tk.Canvas(width=700, height=326, background="black")
        self.canvas.grid(row=0, column=0)


