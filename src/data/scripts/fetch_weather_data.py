import os

from src.data.location_manager import LocationManager
from src.data.data_fetcher import DataFetcher
from src.data.data_manager import DataManager

def main():
  location_manager = LocationManager()
  coordinates = location_manager.get_all_coordinates()
  data_fetcher = DataFetcher(coordinates)
  data_manager = DataManager(os.path.join('data', 'raw', 'weather'))

  weather_data = data_fetcher.get_weather_data()
  timestamp = data_manager.get_last_marine_data_timestamp(os.path.join('data', 'raw', 'marine'))

  data_manager.save_json(weather_data, 'fetched', timestamp)

if __name__ == "__main__":
  main()