from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from screens.widgets.WeatherCard import WeatherCard
from datetime import datetime
import os
from dotenv import load_dotenv

class FiveDayForecastScreen(Screen):
    controller = ObjectProperty(None)
    location_label = StringProperty("5-Day Forecast")  # Default fallback

    def on_enter(self):
        self.ids.forecast_cards.clear_widgets()

        load_dotenv()  # Load environment variables from .env file
        city_name = os.getenv('LOCATION')

        self.location_label = f"5-Day Forecast for {city_name}"

        # Get location key for the city you want
        loc_key = self.controller.get_location_key(city_name)
        if not loc_key:
            print("No location key found")
            return

        forecast = self.controller.get_five_day_forecast(loc_key)
        if not forecast:
            print("No forecast returned")
            return

        for item in forecast:
            card = WeatherCard()
            card.set_data(
                day=item["day"],
                high=item["high"],
                low=item["low"],
                description=item["description"],
                icon_code=item.get("icon_code")  # Use get to avoid KeyError if not present
            )
            self.ids.forecast_cards.add_widget(card)