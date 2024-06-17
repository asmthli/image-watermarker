import tkinter as tk

import ctypes
import platform

from menu import Menu
from image import Image


class UI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Watermarker")
        self.config(background="grey")

        self.image = Image(self)
        self.menu = Menu(self, self.image)

        # Fixes resolution scaling issue in Windows. Without it,
        # tkinter was reporting a scaled resolution and so .winfo_x etc. was wrong.
        if platform.system() == "Windows":
            user32 = ctypes.windll.user32
            user32.SetProcessDPIAware()

    def start_event_loop(self):
        self.mainloop()
