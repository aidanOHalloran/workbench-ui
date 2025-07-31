README.TXT — Kivy App Structure Overview

This file explains how the Kivy framework components work together to create a touchscreen interface.

========================================
| USER INTERACTION FLOW BETWEEN LAYERS |
========================================

This section explains how the app connects:
- Touchscreen UI (KV files)
- Logic containers (Screen classes)
- Backend logic and API/cache handling (Controller)


===================
| COMPONENT ROLES |
===================

1. Screens (ScreenManager and Screen classes)

Manage multiple pages (or views) within the app.

Allow seamless transitions between parts of the UI (e.g., Home, Projects, Weather, etc.).

Each Screen is a container for widgets.

ScreenManager switches between them based on app logic.

***********************************************************
***********************************************************
***********************************************************

from kivy.uix.screenmanager import ScreenManager, Screen

class HomeScreen(Screen):
    pass

class WeatherScreen(Screen):
    pass

***********************************************************
***********************************************************
***********************************************************



===================
| KV FILES (.kv)  |
===================

Define the visual layout and styling of each screen.

Avoid cluttering Python logic with UI code.

Bind visual elements (e.g., buttons, labels) to app properties or events.

Automatically matched to class names if named correctly (e.g., HomeScreen loads from home.kv if specified).

***********************************************************
***********************************************************
***********************************************************
<HomeScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Welcome to the Workbench Info System'
        Button:
            text: 'Go to Weather'
            on_release: app.root.current = 'weather'

***********************************************************
***********************************************************
***********************************************************



=============================
| CONTROLLERS (main .py app) |
=============================

Set up the ScreenManager, load KV files, and handle transitions or events.

Contain the logic for user actions, like button presses or data loading.

Link user input to backend functions (e.g., temperature reading, GPIO input).


***********************************************************
***********************************************************
***********************************************************
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# Load layout definitions
Builder.load_file('home.kv')
Builder.load_file('weather.kv')

class HomeScreen(Screen):
    pass

class WeatherScreen(Screen):
    pass

class WorkbenchApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(WeatherScreen(name='weather'))
        return sm

***********************************************************
***********************************************************
***********************************************************


EXAMPLE FROM THIS APPLICATION: Weather!

==================================================
| EXAMPLE: Weather Menu -> Today’s Forecast Screen |
==================================================

Step-by-step flow:

1. User taps **“Today's Forecast”** button in `WeatherMenuScreen`.


<WeatherMenuScreen>:
    ...
    Button:
        text: "Todays Forecast"
        font_size: 45
        on_release: app.root.current = 'todaysForecast'

→ This triggers a screen change via `ScreenManager`.


2. Kivy switches to `TodaysForecastScreen`. That screen class listens to the `on_enter()` event.

***********************************************************
***********************************************************
***********************************************************

class TodaysForecastScreen(Screen):
    controller = ObjectProperty(None)
    location_label = StringProperty("Today's Forecast")

    def on_enter(self):
        self.ids.hourly_forecast_container.clear_widgets()
        ...

***********************************************************
***********************************************************
***********************************************************


3. Inside `on_enter()`, the screen requests forecast data using the shared controller.

***********************************************************
***********************************************************
***********************************************************

loc_key = self.controller.get_location_key(city_name)
hourly_data = self.controller.get_hourly_forecast(loc_key)

***********************************************************
***********************************************************
***********************************************************

→ This reuses the AccuWeather API controller with caching.


4. The screen dynamically populates a GridLayout with WeatherCard widgets:

***********************************************************
***********************************************************
***********************************************************

for hour in hourly_data:
    card = WeatherCard()
    card.set_data(
        day=hour["time"],
        high=hour["temp"],
        low=hour["temp"],
        description=hour["description"],
        icon_code=hour["icon_code"]
    )
    self.ids.hourly_forecast_container.add_widget(card)

***********************************************************
***********************************************************
***********************************************************

→ The `WeatherCard` is a reusable widget that receives data via `set_data()`.

=======================
| DATA HANDOFF SUMMARY |
=======================

➡ KV File  
- Captures tap via `on_release`  
- Calls `app.root.current = 'todaysForecast'`

➡ Screen Class (`TodaysForecastScreen`)  
- Uses `on_enter()` to trigger logic  
- Talks to controller via `self.controller`

➡ Controller (`WeatherController`)  
- Fetches data from API or cache  
- Returns formatted weather data

➡ Back to Screen  
- Loops through results  
- Builds and displays WeatherCards

================================
| HOW TO CONNECT THE CONTROLLER |
================================

In the main app (e.g. `main.py`), you must connect the controller to each screen:


from screens.weather_menu import WeatherMenuScreen
from screens.weather_today import TodaysForecastScreen
from controller.weather import WeatherController

class WorkbenchApp(App):
    def build(self):
        self.controller = WeatherController(self, apiKey=YOUR_API_KEY)
        sm = ScreenManager()

        weather_menu = WeatherMenuScreen(name='weatherMenu')
        today_screen = TodaysForecastScreen(name='todaysForecast')

        # Set controller reference
        weather_menu.controller = self.controller
        today_screen.controller = self.controller

        sm.add_widget(weather_menu)
        sm.add_widget(today_screen)

        # Let controller access root if needed
        self.controller.root = sm

        return sm
