import os

from src.data.data_manager import DataManager

def preprocess_marine_data(data):
  keys_to_remove = ['generationtime_ms', 'utc_offset_seconds', 'timezone', 'timezone_abbreviation', 'current_units', 'current']

  for marine_data in data:
    if marine_data:
      marine_data['timestamp'] = marine_data['current']['time']
      marine_data['wave_height'] = marine_data['current']['wave_height']
      for key in keys_to_remove:
        marine_data.pop(key, None)

  return data

def main():
  data_manager = DataManager('data')
  marine_data, timestamp = data_manager.get_latest_json_and_timestamp(os.path.join('raw', 'marine'), 'fetched')
  preprocessed_marine_data = preprocess_marine_data(marine_data)
  data_manager.save_json(preprocessed_marine_data, 'preprocessed', timestamp, os.path.join('preprocessed', 'marine'))
  
  print(f'Marine data preprocessed and saved to {os.path.join("data", "preprocessed", "marine", f"preprocessed_data_{timestamp}.json")}')

if __name__ == "__main__":
  main()