import requests

class DataFetcher:
  weather_api_url = "https://api.open-meteo.com/v1/forecast"
  marine_api_url = "https://marine-api.open-meteo.com/v1/marine"
  timezone = "Europe/Berlin"

  weather_variables = ["temperature_2m", "wind_speed_10m", "wind_direction_10m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature", "precipitation_probability", "rain", "surface_pressure"]
  marine_variables = ["wave_height"]

  def __init__(self, coordinates):
    self.coordinates = coordinates
  
  def get_weather_data(self):
    params = {
      "latitude": self.coordinates[0],
      "longitude": self.coordinates[1],
      "hourly": self.weather_variables,
      "timezone": self.timezone,
      "forecast_days": 1,
      "timeformat": "unixtime"
    }

    weather_response = requests.get(self.weather_api_url, params=params)
    weather_data = weather_response.json()
    return weather_data
  
  def get_marine_data(self):
    params = {
      "latitude": self.coordinates[0],
      "longitude": self.coordinates[1],
      "timezone": self.timezone,
      "current": self.marine_variables,
      "timeformat": "unixtime"
    }

    marine_response = requests.get(self.marine_api_url, params=params)
    marine_data = marine_response.json()
    return marine_data