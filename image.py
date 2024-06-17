import tkinter as tk

import PIL.Image
import PIL.ImageTk
import PIL.ImageGrab


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

        self.selected_item = self.enable_selection()

        self.watermark_logo_img = None
        self.watermark = None

        self.logo_text_ids = []
        self.text_size = tk.IntVar(value=12)

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

    def enable_selection(self):
        def select(event):
            self.selected_item = self.image_canvas.find_closest(event.x, event.y)[0]
            print("selected: ", self.selected_item)

        self.image_canvas.tag_bind(tagOrId="selectable", sequence="<ButtonPress-1>", func=select)

        return 0

    def load_image(self, filepath):
        self.watermark_logo_img = PIL.Image.open(filepath)
        resized_image = self.watermark_logo_img.resize(size=(self.canvas_size_width, self.canvas_size_height))

        # Image must be referenced otherwise it is garbage collected after the method returns and will not
        # be shown in the canvas. Here we attach it to the image canvas itself (makes more sense than attaching it to
        # self).
        self.image_canvas.background_img = PIL.ImageTk.PhotoImage(image=resized_image)
        self.image_canvas.create_image(0, 0, anchor="nw", image=self.image_canvas.background_img)

    def add_watermark_logo(self, filepath):
        self.watermark_logo_img = PIL.Image.open(filepath)

        resized_image = self.watermark_logo_img.resize(size=(self.canvas_size_width // 4, self.canvas_size_height // 4))

        # Needs a reference to prevent garbage collection.
        self.image_canvas.watermark_logo_tkImage = PIL.ImageTk.PhotoImage(image=resized_image)
        self.watermark = self.image_canvas.create_image(0, 0,
                                                        anchor="nw",
                                                        image=self.image_canvas.watermark_logo_tkImage,
                                                        tags=("draggable",
                                                              "selectable"))
