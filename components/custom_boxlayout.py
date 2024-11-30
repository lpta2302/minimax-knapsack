from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

class CustomBoxLayout(BoxLayout):
    def __init__(self,color = (0,0,0,.6), **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*color)  # Green color (RGBA, each value between 0 and 1)
            self.rect = Rectangle(
                size=self.size, 
                pos=self.pos)

        # Bind the size and pos properties to update the rectangle when the widget changes
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, instance, value):
        # Update the rectangle's size and position based on the widget's current size and position
        self.rect.size = self.size
        self.rect.pos = self.pos
