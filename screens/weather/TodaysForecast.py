from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from screens.widgets.WeatherCard import WeatherCard
import os
from dotenv import load_dotenv

class TodaysForecastScreen(Screen):
    controller = ObjectProperty(None)
    location_label = StringProperty("Today's Forecast")  # Default fallback

    def on_enter(self):
        self.ids.hourly_forecast_container.clear_widgets()

        load_dotenv()
        city_name = os.getenv("LOCATION", "Mobile, AL")

        self.location_label = f"Today's Forecast for {city_name}"

        loc_key = self.controller.get_location_key(city_name)
        if not loc_key:
            print("No location key found")
            return

        hourly_data = self.controller.get_hourly_forecast(loc_key)
        if not hourly_data:
            print("No hourly data returned")
            return

        for hour in hourly_data:
            card = WeatherCard()
            card.set_data(
                day=hour["time"],
                high=hour["temp"],
                low=hour["temp"],  # For hourly, high/low are the same
                description=hour["description"],
                icon_code=hour["icon_code"]
            )
            self.ids.hourly_forecast_container.add_widget(card)
