from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.button import Button
from kivy.app import App

class ProjectCard(BoxLayout):
    def __init__(self, title, description, category, size_hint_y=None, height=160, **kwargs):
        # Save the title and category so we can use them when deleting
        self.title = title
        self.category = category

        # Set up the base layout
        super().__init__(
            orientation='vertical',
            padding=(10, 5),
            spacing=5,
            size_hint_y=None,
            height=160,  # adjust height to fit delete button
            **kwargs
        )

        # Add a light gray rounded rectangle background
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.bg = RoundedRectangle(radius=[10], pos=self.pos, size=self.size)

        # Ensure the background resizes with the widget
        self.bind(pos=self._update_bg, size=self._update_bg)
        self.bind(children=lambda *x: self._update_bg())

        # Add title label
        self.add_widget(Label(
            text=title,
            font_size=30,
            bold=True,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=40,
            halign='left',
            valign='middle',
            text_size=(800, None)
        ))

        # Add description label
        self.add_widget(Label(
            text=description,
            font_size=25,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=60,
            halign='left',
            valign='top',
            text_size=(800, None)
        ))

        # Add delete button
        delete_btn = Button(
            text="Delete",
            size_hint_y=None,
            height=40,
            font_size=20,
            background_color=(1, 0.3, 0.3, 1)  # red-tinted button
        )
        delete_btn.bind(on_release=self.delete_project)
        self.add_widget(delete_btn)

    def delete_project(self, instance):
        # Call the app-level controller method to delete this project
        app = App.get_running_app()
        app.projectController.DeleteProject(self.title, self.category)

    def _update_bg(self, *args):
        # Keep the background rectangle aligned with widget size
        self.bg.pos = self.pos
        self.bg.size = self.size
