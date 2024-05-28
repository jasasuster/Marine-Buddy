import os

from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

from src.data.data_manager import DataManager
from src.data.location_manager import LocationManager

def merge_data(marine_data, weather_data, location_names):
  merged_data = [
    {**marine_data_object, **weather_data_object}
    for marine_data_object, weather_data_object in zip(marine_data, weather_data)
  ]

  for index, merged_data_object in enumerate(merged_data):
    merged_data_object['location_name'] = location_names[index]

  return merged_data

def save_merged_data(data_manager, merged_data):
  for merged_data_object in merged_data:
    file_name = merged_data_object['location_name'].replace(' ', '_').lower()
    data_manager.save_csv('processed', merged_data_object, file_name)

def main():
  location_manager = LocationManager()
  location_names = location_manager.get_location_names()

  data_manager = DataManager('data')
  marine_data, marine_timestamp = data_manager.get_latest_json_and_timestamp(os.path.join('preprocessed', 'marine'), 'preprocessed')
  weather_data, weather_timestamp = data_manager.get_latest_json_and_timestamp(os.path.join('preprocessed', 'weather'), 'preprocessed')

  if not (marine_data and weather_data and marine_timestamp == weather_timestamp):
    print('No data to merge')
  else:
    merged_data = merge_data(marine_data, weather_data, location_names)
    save_merged_data(data_manager, merged_data)
    print(f'Merged data saved to {os.path.join("data", "processed")}')