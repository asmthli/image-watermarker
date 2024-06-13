import tkinter as tk


class UI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Watermarker")
        self.config(background="grey")

        self.image = Image(self)
        self.menu = Menu(self)

    def start_event_loop(self):
        self.mainloop()


class Menu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Canvas(master=self, width=800, height=100, background="indigo").pack()
        self.pack()


class Image(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Canvas(master=self, width=700, height=326, background="black").pack()
        self.pack()
