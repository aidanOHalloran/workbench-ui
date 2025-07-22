import json
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class ProjectController:
    def __init__(self, app):
        self.app = app
        self.root = None  # This will be set to the root of the app later

    def AddProject(self, title, description, category):
        if not title or not description or category not in ["current", "planned", "past"]:
            print("Invalid input")
            return

        path = "data/projects.json"
        try:
            with open(path, "r") as f:
                data = json.load(f)
            data[category].append({
                "title": title,
                "description": description
            })
            with open(path, "w") as f:
                json.dump(data, f, indent=2)
            print("Project added!")
        except Exception as e:
            print(f"Error adding project: {e}")

        # Get screen before using it
        screen = self.root.get_screen('addProjectPage')

        # Clear fields
        screen.ids.title_input.text = ""
        screen.ids.description_input.text = ""
        screen.ids.category_spinner.text = "Select Category"
        screen.ids.title_input.focus = False
        screen.ids.description_input.focus = False

        # Show confirmation popup
        self.show_confirmation_popup()

        # Return to main projects screen
        self.root.current = 'projects'

    def show_confirmation_popup(self, message="Project added!"):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        label = Label(text=message, font_size=60)
        btn = Button(text="OK", size_hint_y=None, height=50, font_size=40)

        layout.add_widget(label)
        layout.add_widget(btn)

        popup = Popup(title="Success", content=layout, size_hint=(None, None), size=(400, 250), auto_dismiss=False)
        btn.bind(on_release=popup.dismiss)
        popup.open()