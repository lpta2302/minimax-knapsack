from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window

class HoverBehavior:
    """
    A mixin that adds hover effects to widgets.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.hovered = False

    def on_mouse_pos(self, instance, pos):
        if not self.get_root_window():
            return  # Widget is not visible

        is_hovering = self.collide_point(*self.to_widget(*pos))
        if is_hovering and not self.hovered:
            self.on_hover_enter()
            self.hovered = True
        elif not is_hovering and self.hovered:
            self.on_hover_leave()
            self.hovered = False

    def on_hover_enter(self):
        """Called when the mouse enters the widget area."""
        pass

    def on_hover_leave(self):
        """Called when the mouse leaves the widget area."""
        pass

class HoverButton(Button, HoverBehavior):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.default_color = self.background_color
        self.hover_color = [0.7, 0.7, 0.7, 1]  # Gray hover effect

    def on_hover_enter(self):
        self.background_color = self.hover_color

    def on_hover_leave(self):
        self.background_color = self.default_color
