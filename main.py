from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'dock')

from dotenv import load_dotenv
import os

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

# HOME IMPORTS
from screens.home import HomeScreen
# PROJECTS IMPORTS
from screens.projects.Projects import ProjectsScreen
from screens.projects.CurrentProjects import CurrentProjectsScreen
from screens.projects.PlannedProjects import PlannedProjectsScreen
from screens.projects.PastProjects import PastProjectsScreen
from screens.projects.AddProject import AddProjectScreen

# WHITEBOARD IMPORTS
from screens.whiteboard.Whiteboard import WhiteboardScreen

# WEATHER IMPORTS
from screens.weather.WeatherMenu import WeatherMenuScreen
from screens.weather.TodaysForecast import TodaysForecastScreen
from screens.weather.FiveDayForecast import FiveDayForecastScreen

# CONTROLLER IMPORTS
from controllers import ProjectController
from controllers import KeyboardController
from controllers.WeatherController import WeatherController
from controllers.KeyboardController import TouchInput
from kivy.factory import Factory
Factory.register('TouchInput', cls=TouchInput)

class WorkbenchApp(App):
    # Here set functions for different controller actions

    # KEYBOARD CONTROLLER METHODS

    # PROJECT CONTROLLER METHODS
    def AddProject(self, title, description, category):
        self.projectController.AddProject(title, description, category)
        # Clear form and navigate back
        screen = self.root.get_screen('addProjectPage')
        screen.ids.title_input.text = ""
        screen.ids.description_input.text = ""
        screen.ids.category_spinner.text = "Select Category"
        self.root.current = 'projects'

    # Build the actual app itself w/ screens and .kv files
    def build(self):
        self.projectController = ProjectController.ProjectController(self) # create instance of ProjectController
        self.keyboardController = KeyboardController.KeyboardController(self) # create instance of KeyboardController

        load_dotenv()  # Load environment variables from .env file
        weatherKey = os.getenv('WEATHER_KEY')

        self.weatherController = WeatherController(self, apiKey = weatherKey)  # create instance of WeatherController

        # Load .kv files for screens
        Builder.load_file('kv/home.kv')

        # Load .kv files for project screens
        Builder.load_file('kv/projects/projects.kv')
        Builder.load_file('kv/projects/currentProjects.kv')
        Builder.load_file('kv/projects/plannedProjects.kv')
        Builder.load_file('kv/projects/pastProjects.kv')
        Builder.load_file('kv/projects/addProject.kv')

        # Load .kv file for whiteboard screen
        Builder.load_file('kv/whiteboard/whiteboard.kv')

        # Load .kv file for weather menu screen
        Builder.load_file('kv/weather/weatherMenu.kv')
        Builder.load_file('kv/weather/todaysForecast.kv')
        Builder.load_file('kv/weather/fiveDayForecast.kv')


        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        
        # PROJECT SCREENS
        sm.add_widget(ProjectsScreen(name='projects'))
        sm.add_widget(CurrentProjectsScreen(name='currentProjects'))
        sm.add_widget(PlannedProjectsScreen(name='plannedProjects'))
        sm.add_widget(PastProjectsScreen(name='pastProjects'))
        sm.add_widget(AddProjectScreen(name='addProjectPage'))

        # WHITEBOARD SCREEN
        sm.add_widget(WhiteboardScreen(name='whiteboard'))

        # WEATHER SCREENS
        # Create weather screens and inject controller
        weather_menu = WeatherMenuScreen(name='weatherMenu')
        weather_menu.controller = self.weatherController

        today_screen = TodaysForecastScreen(name='todaysForecast')
        today_screen.controller = self.weatherController

        week_screen = FiveDayForecastScreen(name='fiveDayForecast')
        week_screen.controller = self.weatherController

        # Add screens to ScreenManager
        sm.add_widget(weather_menu)
        sm.add_widget(today_screen)
        sm.add_widget(week_screen)

        # Set root for controllers so they can access screens
        self.projectController.root = sm
        self.keyboardController.root = sm
        self.weatherController.root = sm

        return sm

# Run App
if __name__ == '__main__':
    WorkbenchApp().run()