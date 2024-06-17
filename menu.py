import tkinter as tk

from tkinter import filedialog, colorchooser

import re

from image import Image

import PIL
from PIL import ImageTk, ImageGrab


class Menu(tk.Frame):
    def __init__(self, parent, image: Image):
        super().__init__(parent)
        self.text_entry = None
        self.add_text_btn = None

        self.image = image
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.text_entry = tk.Entry(master=self)
        self.text_entry.pack()

        self.create_load_img_btn()
        self.create_add_text_btn()
        self.create_save_img_btn()
        self.create_add_logo_btn()
        self.create_text_colour_btn()

        self.create_size_slider()

        self.create_text_size_spinner()

    def create_add_text_btn(self):
        def add_text():
            text_id = self.image.image_canvas.create_text(20,
                                                          20,
                                                          text=self.text_entry.get(),
                                                          fill="white",
                                                          font=14,
                                                          tags=("draggable",))
            self.image.logo_text_ids.append(text_id)

        tk.Button(master=self, text="Add Text", command=add_text).pack()

    def create_text_colour_btn(self):
        def choose_text_colour():
            colour_hex = tk.colorchooser.askcolor()[1]

            for id_ in self.image.logo_text_ids:
                self.image.image_canvas.itemconfigure(id_, fill=colour_hex)

        tk.Button(master=self, text="Choose Text Colour", command=choose_text_colour).pack()

    def create_text_size_spinner(self):
        def change_font_sizes():
            for id_ in self.image.logo_text_ids:
                self.image.image_canvas.itemconfigure(id_, font=("Arial Baltic", self.image.text_size.get()))

        tk.Spinbox(master=self, command=change_font_sizes, textvariable=self.image.text_size, from_=1, to=20).pack()

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

    def create_add_logo_btn(self):
        def choose_logo_dialogue():
            file_path = filedialog.askopenfilename()
            if file_path:
                self.image.add_watermark_logo(file_path)

        tk.Button(master=self, text="Add Logo", command=choose_logo_dialogue).pack()

    def create_size_slider(self):
        def adjust_watermark_img_size(event_slide_value):
            event_slide_value = int(event_slide_value)
            new_width = event_slide_value * 40
            new_height = event_slide_value * 30

            resized_image = self.image.watermark_logo_img.resize(size=(new_width, new_height))
            resized_tkImage = PIL.ImageTk.PhotoImage(image=resized_image)
            # Again needs to be referenced, so it isn't garbage collected.
            self.image.image_canvas.watermark_logo = resized_tkImage
            self.image.image_canvas.itemconfigure(self.image.watermark, image=resized_tkImage)

        slider = tk.Scale(master=self,
                          orient="horizontal",
                          command=adjust_watermark_img_size,
                          from_=1,
                          to=100,
                          variable=tk.IntVar(value=50))
        slider.pack()