from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle
from kivy.uix.image import Image

class Background(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            # Add a rectangle with a background image
            self.rect = Rectangle(
                source='./images/background.jpeg',  # Path to the image
                size=self.size,  # Size of the widget
                pos=self.pos  # Position of the widget
            )

    def on_size(self, *args):
        # Update the background size when the widget size changes
        self.rect.size = self.size

    def on_pos(self, *args):
        # Update the background position when the widget position changes
        self.rect.pos = self.pos
