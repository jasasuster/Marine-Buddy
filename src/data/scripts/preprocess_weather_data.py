import os

from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

from src.data.data_manager import DataManager

def hour_rounder(t):
  # Rounds to nearest hour by adding a timedelta hour if minute >= 30
  return int((t.replace(second=0, microsecond=0, minute=0, hour=t.hour) + timedelta(hours=t.minute // 30)).timestamp())

def preprocess_weather_data(data):
  rounded_time = hour_rounder(datetime.now(ZoneInfo("Europe/Berlin")))
  closest_weater_data_list = []

  forecast_times = data[0]['hourly']['time']
  if rounded_time not in forecast_times:
    rounded_time = forecast_times[0]

  for forecast_object in data:
    if forecast_object:
      weather_data = forecast_object['hourly']
      closest_weather_data = {key: value[forecast_times.index(rounded_time)] for key, value in weather_data.items() if key != 'time'}
      closest_weater_data_list.append(closest_weather_data)

  return closest_weater_data_list

def main():
  data_manager = DataManager('data')
  weather_data, timestamp = data_manager.get_latest_json_and_timestamp(os.path.join('raw', 'weather'), 'fetched')
  preprocessed_weather_data = preprocess_weather_data(weather_data)
  data_manager.save_json(preprocessed_weather_data, 'preprocessed', timestamp, os.path.join('preprocessed', 'weather'))

if __name__ == "__main__":
  main()