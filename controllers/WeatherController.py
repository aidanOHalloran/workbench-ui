import requests
from datetime import datetime
import time

class WeatherController:
    def __init__(self, app, apiKey):
        self.app = app
        self.apiKey = apiKey
        self.root = None  # set externally to ScreenManager
        self.location_cache = {}  # to avoid duplicate lookups
        self.cache = {
            "current_conditions": {"data": None, "timestamp": 0},
            "hourly_forecast": {"data": None, "timestamp": 0},
            "five_day_forecast": {"data": None, "timestamp": 0}
        }

    def get_location_key(self, city_name):
        if city_name in self.location_cache:
            return self.location_cache[city_name]

        url = "https://dataservice.accuweather.com/locations/v1/cities/search"
        params = {
            "apikey": self.apiKey,
            "q": city_name
        }

        try:
            res = requests.get(url, params=params)
            res.raise_for_status()
            data = res.json()
            if not data:
                print("No location data returned.")
                return None
            key = data[0]["Key"]
            self.location_cache[city_name] = key
            return key
        except Exception as e:
            print(f"Error fetching location key: {e}")
            return None

    def get_current_conditions(self, location_key):
        now = time.time()
        cache_entry = self.cache["current_conditions"]

        if cache_entry["data"] and now - cache_entry["timestamp"] < 1200:  # 20 mins = 1200 seconds
            return cache_entry["data"]

        url = f"https://dataservice.accuweather.com/currentconditions/v1/{location_key}"
        params = {"apikey": self.apiKey}

        try:
            res = requests.get(url, params=params)
            res.raise_for_status()
            data = res.json()
            if data:
                current = data[0]
                parsed = [
                    {
                        "temperature": current["Temperature"]["Imperial"]["Value"],
                        "text": current["WeatherText"],
                        "is_day": current["IsDayTime"]
                    }
                ]

                # Update cache
                self.cache["current_conditions"] = {"data": parsed, "timestamp": now}
                return parsed
        except Exception as e:
            print(f"Error fetching current conditions: {e}")

        return None

    def get_hourly_forecast(self, location_key):
        now = time.time()
        cache_entry = self.cache["hourly_forecast"]

        if cache_entry["data"] and now - cache_entry["timestamp"] < 1200:  # 20 mins = 1200 seconds
            return cache_entry["data"]

        url = f"https://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{location_key}"
        params = {
            "apikey": self.apiKey,
            "details": "true"
        }

        try:
            res = requests.get(url, params=params)
            res.raise_for_status()
            data = res.json()
            parsed = [
                {
                    "time": self._format_time(hour["DateTime"]),
                    "temp": hour["Temperature"]["Value"],
                    "description": hour["IconPhrase"],
                    "icon_code": hour["WeatherIcon"]
                }
                for hour in data
            ]

            # Update cache
            self.cache["hourly_forecast"] = {"data": parsed, "timestamp": now}
            return parsed
        except Exception as e:
            print(f"Error fetching hourly forecast: {e}")
            return []

    def get_five_day_forecast(self, location_key):
        now = time.time()
        cache_entry = self.cache["five_day_forecast"]

        if cache_entry["data"] and now - cache_entry["timestamp"] < 1200:  # 20 mins = 1200 seconds
            return cache_entry["data"]

        url = f"https://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}"
        params = {
            "apikey": self.apiKey,
            "details": "true"
        }

        try:
            res = requests.get(url, params=params)
            res.raise_for_status()
            data = res.json()
            parsed = [
                {
                    "day": self._format_day(day["Date"]),
                    "high": day["Temperature"]["Maximum"]["Value"],
                    "low": day["Temperature"]["Minimum"]["Value"],
                    "description": day["Day"]["IconPhrase"],
                    "icon_code": day["Day"]["Icon"]
                }
                for day in data["DailyForecasts"]
            ]

            # Update cache
            self.cache["five_day_forecast"] = {"data": parsed, "timestamp": now}
            return parsed

        except Exception as e:
            print(f"Error fetching 5-day forecast: {e}")
            return []

    def _format_day(self, iso_string):
        dt = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S%z")
        return dt.strftime("%A")

    def _format_time(self, iso_string):
        dt = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S%z")
        return dt.strftime("%I %p").lstrip("0")