from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.properties import ListProperty


class CanvasWidget(Widget):
    line_color = ListProperty([1, 1, 1])  # white as default

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Keep track of all Line graphics objects so we can undo or clear them later
        self.lines = []

    def on_touch_down(self, touch):
        # Start a new line only if the touch is inside this widget's bounds
        if self.collide_point(*touch.pos):
            with self.canvas:
                # Set the drawing color based on the current selected line_color
                Color(*self.line_color)
                # Create a new line starting at the touch location
                line = Line(points=(touch.x, touch.y), width=2)
                # Store the line in the touch object so we can continue it during movement
                touch.ud['line'] = line
                # Also keep track of the line in our local list for undo/clear
                self.lines.append(line)

    def on_touch_move(self, touch):
        # When the touch moves, continue the current line by adding new points
        if 'line' in touch.ud:
            touch.ud['line'].points += (touch.x, touch.y)

    def clear_canvas(self):
        # Remove all drawing instructions from the canvas
        self.canvas.clear()
        # Reset the list of stored lines
        self.lines.clear()

    def undo_last(self):
        # Remove the most recently drawn line if any exist
        if self.lines:
            last_line = self.lines.pop()      # Remove from tracking
            self.canvas.remove(last_line)     # Remove from the actual canvas

    def set_color(self, r, g, b):
        # Set the drawing color to use for the next lines
        self.line_color = [r, g, b]