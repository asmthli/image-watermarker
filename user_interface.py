import tkinter as tk
from tkinter import filedialog

import PIL.Image
import PIL.ImageTk
import PIL.ImageGrab

import re

import ctypes
import platform


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


class Image(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvas_size_width = 800
        self.canvas_size_height = 526
        self.image_canvas = tk.Canvas(master=self,
                                      width=self.canvas_size_width,
                                      height=self.canvas_size_height,
                                      background="black")
        self.image_canvas.pack()
        self.pack()

        # Keeps track of an item being dragged on the canvas.
        self.drag_data = self.enable_dragging()

    def enable_dragging(self):
        """Adds event handling for dragging on any element added to the image canvas with tag 'draggable'.

        :return Dictionary storing information about the item being dragged."""

        def drag_start(event):
            self.drag_data["item"] = self.image_canvas.find_closest(event.x, event.y)[0]
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

        def drag_stop(event):
            self.drag_data["item"] = None
            self.drag_data["x"] = 0
            self.drag_data["y"] = 0

        def drag(event):
            delta_x = event.x - self.drag_data["x"]
            delta_y = event.y - self.drag_data["y"]
            self.image_canvas.move(self.drag_data["item"], delta_x, delta_y)
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

        self.image_canvas.tag_bind(tagOrId="draggable", sequence="<ButtonPress-1>", func=drag_start)
        self.image_canvas.tag_bind(tagOrId="draggable", sequence="<ButtonRelease-1>", func=drag_stop)
        self.image_canvas.tag_bind(tagOrId="draggable", sequence="<B1-Motion>", func=drag)

        # Used to keep track of item being dragged.
        drag_data = {"x": 0,
                     "y": 0,
                     "item": None}

        return drag_data

    def load_image(self, filepath):
        image = PIL.Image.open(filepath)
        resized_image = image.resize(size=(self.canvas_size_width, self.canvas_size_height))
        tkImage = PIL.ImageTk.PhotoImage(image=resized_image)

        # Image must be referenced otherwise it is garbage collected after the method returns and will not
        # be shown in the canvas. Here we attach it to the image canvas itself (makes more sense than attaching it to
        # self).
        self.image_canvas.image = tkImage
        self.image_canvas.create_image(0, 0, anchor="nw", image=tkImage)


class Menu(tk.Frame):
    def __init__(self, parent, image: Image):
        super().__init__(parent)
        self.text_entry = None
        self.add_text_btn = None

        self.pack()
        self.create_widgets()
        self.image = image

    def create_widgets(self):
        self.text_entry = tk.Entry(master=self)
        self.text_entry.pack()

        self.create_load_img_btn()
        self.create_add_text_btn()
        self.create_save_img_btn()

    def create_add_text_btn(self):
        def add_text():
            self.image.image_canvas.create_text(20,
                                                20,
                                                text=self.text_entry.get(),
                                                fill="white",
                                                font=14,
                                                tags=("draggable",))

        tk.Button(master=self, text="Add Text", command=add_text).pack()

    def create_save_img_btn(self):
        def save_image():
            # There is no way to get file extension here. It simply filters the file types shown.
            file_path = filedialog.asksaveasfilename(filetypes=(('PNG File', '.png'),))
            # Raw string literal (with r prefix) is used to escape the '.' wildcard operator for regex.
            if re.search(pattern="." + r"." + "png", string=file_path) is None:
                file_path += ".png"

            self.image.update_idletasks()
            x0 = self.image.image_canvas.winfo_rootx()
            y0 = self.image.image_canvas.winfo_rooty()
            x1 = x0 + self.image.image_canvas.winfo_width()
            y1 = y0 + self.image.image_canvas.winfo_height()

            PIL.ImageGrab.grab(bbox=(x0, y0, x1, y1)).save(fp=file_path,)

        tk.Button(master=self, text="Save Image", command=save_image).pack()

    def create_load_img_btn(self):
        def choose_img_dialogue():
            file_path = filedialog.askopenfilename()
            if file_path:
                self.image.load_image(file_path)

        tk.Button(master=self, text="Load Image", command=choose_img_dialogue).pack()
