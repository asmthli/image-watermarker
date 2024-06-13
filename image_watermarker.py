from user_interface import UI


class ImageWatermarker:
    def __init__(self):
        self.ui = UI()

    def run(self):
        self.ui.start_event_loop()


if __name__ == "__main__":
    watermarker = ImageWatermarker()
    watermarker.run()
