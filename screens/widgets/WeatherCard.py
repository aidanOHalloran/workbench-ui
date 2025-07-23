from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.app import App
from kivy.uix.image import Image

class WeatherCard(BoxLayout):
    def __init__(self, **kwargs):

        
        # Set up the base layout
        super().__init__(
            orientation='horizontal',
            padding=(10, 5),
            spacing=5,
            size_hint_y=None,
            height=160,
            **kwargs
        )

        # Add a light gray rounded rectangle background
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.bg = RoundedRectangle(radius=[10], pos=self.pos, size=self.size)

        # Ensure the background resizes with the widget
        self.bind(pos=self._update_bg, size=self._update_bg)
        
        # Create icon
        self.icon = Image(size_hint=(None, 1), width=100)

        # Create label block
        label_box = BoxLayout(orientation='vertical', spacing=5, padding=[0, 10, 0, 0]) # [left, top, right, bottom] — moves it up slightly

        self.day_label = Label(font_size=35, size_hint_y=None, height=30, color=(0, 0, 0, 1))
        self.temp_label = Label(font_size=30, size_hint_y=None, height=30, color=(0, 0, 0, 1))
        self.desc_label = Label(font_size=28, size_hint_y=None, height=30, color=(0, 0, 0, 1))

        label_box.add_widget(self.day_label)
        label_box.add_widget(self.temp_label)
        label_box.add_widget(self.desc_label)

        # Add icon and labels to main layout
        self.add_widget(self.icon)      # icon on the left
        self.add_widget(label_box)      # text on the right

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def set_data(self, day, high, low, description, icon_code=None):
        self.day_label.text = day
        self.temp_label.text = f"High: {high}°F  |  Low: {low}°F"
        self.desc_label.text = description.capitalize()

        if icon_code is not None:
            # Ensure two-digit filename (e.g., 01.png)
            filename = f"{int(icon_code):02}.png"
            # if filename starts with 0, remove the leading zero
            if filename.startswith("0"):
                filename = filename[1:]
            # Set the icon source
            self.icon.source = f"assets/weatherIcons/{filename}"