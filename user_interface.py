import tkinter as tk
from tkinter import filedialog

import PIL.Image
import PIL.ImageTk


class UI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Watermarker")
        self.config(background="grey")

        self.image = Image(self)
        self.menu = Menu(self, self.image)

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
        self.pack()
        self.create_widgets()
        self.image = image

    def create_widgets(self):
        self.create_load_img_btn()

    def create_load_img_btn(self):
        def choose_img_dialogue():
            file_path = filedialog.askopenfilename()
            if file_path:
                self.image.load_image(file_path)

        tk.Button(master=self, text="Button", command=choose_img_dialogue).pack()



