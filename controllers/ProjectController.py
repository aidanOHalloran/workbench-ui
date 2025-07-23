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
        # Validate inputs
        if not title or not description or category not in ["current", "planned", "past"]:
            print("Invalid input")
            return

        path = "data/projects.json"
        try:
            # Load current project data
            with open(path, "r") as f:
                data = json.load(f)

            # Add the new project to the appropriate category
            data[category].append({
                "title": title,
                "description": description
            })

            # Save updated data
            with open(path, "w") as f:
                json.dump(data, f, indent=2)

            print("Project added!")

        except Exception as e:
            print(f"Error adding project: {e}")
            return  # Exit early on failure

        # Reset the add form UI
        screen = self.root.get_screen('addProjectPage')
        screen.ids.title_input.text = ""
        screen.ids.description_input.text = ""
        screen.ids.category_spinner.text = "Select Category"
        screen.ids.title_input.focus = False
        screen.ids.description_input.focus = False

        # Refresh the project list on confirmation popup close
        refresh_screen = self.root.get_screen(f"{category}Projects")
        self.show_confirmation_popup(message="Project added!", on_close=refresh_screen.on_pre_enter)

    def DeleteProject(self, title, category):
        # Validate input
        if not title or category not in ["current", "planned", "past"]:
            print("Invalid input")
            return

        path = "data/projects.json"
        try:
            # Load current project data
            with open(path, "r") as f:
                data = json.load(f)

            # Remove project with matching title
            data[category] = [proj for proj in data[category] if proj["title"] != title]

            # Save changes
            with open(path, "w") as f:
                json.dump(data, f, indent=2)

            print("Project deleted!")

        except Exception as e:
            print(f"Error deleting project: {e}")
            return  # Exit early on failure

        # Refresh the relevant project screen after popup dismiss
        refresh_screen = self.root.get_screen(f"{category}Projects")
        self.show_confirmation_popup(message="Project deleted!", on_close=refresh_screen.on_pre_enter)

    def show_confirmation_popup(self, message="Project added!", on_close=None):
        # Layout for the popup
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        label = Label(text=message, font_size=60)
        btn = Button(text="OK", size_hint_y=None, height=50, font_size=40)

        layout.add_widget(label)
        layout.add_widget(btn)

        # Create and configure the popup
        popup = Popup(
            title="Success",
            content=layout,
            size_hint=(None, None),
            size=(400, 250),
            auto_dismiss=False
        )

        # Close popup on button press
        btn.bind(on_release=popup.dismiss)

        # Optional callback when popup is dismissed
        if on_close:
            popup.bind(on_dismiss=lambda *args: on_close())

        # Open the popup
        popup.open()