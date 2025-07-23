from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.properties import ListProperty


class CanvasWidget(Widget):
    line_color = ListProperty([1, 1, 1])  # white as default

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lines = []  # Store references to Line instructions

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            with self.canvas:
                Color(*self.line_color)
                line = Line(points=(touch.x, touch.y), width=2)
                touch.ud['line'] = line
                self.lines.append(line)

    def on_touch_move(self, touch):
        if 'line' in touch.ud:
            touch.ud['line'].points += (touch.x, touch.y)

    def clear_canvas(self):
        self.canvas.clear()
        self.lines.clear()

    def undo_last(self):
        if self.lines:
            last_line = self.lines.pop()
            self.canvas.remove(last_line)

    def set_color(self, r, g, b):
        self.line_color = [r, g, b]