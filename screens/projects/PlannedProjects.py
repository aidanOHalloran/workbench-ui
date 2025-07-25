import json
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from screens.widgets.projectCard import ProjectCard


class PlannedProjectsScreen(Screen):
    def on_pre_enter(self):
        self.ids.planned_project_list.clear_widgets()

        with open("data/projects.json", "r") as f:
            data = json.load(f)

        for project in data.get("planned", []):
            card = ProjectCard(project['title'], project['description'], 'planned')
            self.ids.planned_project_list.add_widget(card)
