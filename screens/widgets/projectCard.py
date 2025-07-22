from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle

class ProjectCard(BoxLayout):
    def __init__(self, title, description, **kwargs):
        super().__init__(orientation='vertical', padding=(10, 5), spacing=5, size_hint_y=None, height=110, **kwargs)

        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # light gray for visibility
            self.bg = RoundedRectangle(radius=[10], pos=self.pos, size=self.size)

        self.bind(pos=self._update_bg, size=self._update_bg)
        self.bind(children=lambda *x: self._update_bg())  # ensure refresh

        self.add_widget(Label(
            text=title,
            font_size=30,
            bold=True,
            color=(0, 0, 0, 1),  # black text
            size_hint_y=None,
            height=40,
            halign='left',
            valign='middle',
            text_size=(800, None)
        ))

        self.add_widget(Label(
            text=description,
            font_size=25,
            color=(0, 0, 0, 1),  # black text
            size_hint_y=None,
            height=60,
            halign='left',
            valign='top',
            text_size=(800, None)
        ))

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
