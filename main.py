from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

from screens.home import HomeScreen
from screens.projects.Projects import ProjectsScreen
from screens.projects.CurrentProjects import CurrentProjectsScreen
from screens.projects.PlannedProjects import PlannedProjectsScreen
from screens.projects.PastProjects import PastProjectsScreen

class WorkbenchApp(App):
    def build(self):
        Builder.load_file('kv/home.kv')
        Builder.load_file('kv/projects.kv')
        Builder.load_file('kv/projects/currentProjects.kv')
        Builder.load_file('kv/projects/plannedProjects.kv')
        Builder.load_file('kv/projects/pastProjects.kv')

        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(ProjectsScreen(name='projects'))
        sm.add_widget(CurrentProjectsScreen(name='currentProjects'))
        sm.add_widget(PlannedProjectsScreen(name='plannedProjects'))
        sm.add_widget(PastProjectsScreen(name='pastProjects'))
        return sm

if __name__ == '__main__':
    WorkbenchApp().run()