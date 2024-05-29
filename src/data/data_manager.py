import os
import re
import csv
import json

import pandas as pd

class DataManager:
  def __init__(self, data_path):
    self.data_path = data_path

  def _get_timestamp(self, file_name, data_type = 'fetched'):
    match = re.search(data_type + r'_data_(\d+)', file_name)
    if match:
      return int(match.group(1))
    return None

  def save_json(self, data, data_type, timestamp, additional_path = ''):
    save_path = os.path.join(self.data_path, additional_path)
    os.makedirs(save_path, exist_ok=True)
    raw_output_file_path = os.path.join(save_path, f'{data_type}_data_{timestamp}.json')
    with open(raw_output_file_path, 'w', encoding='utf-8') as file:
      json.dump(data, file, ensure_ascii=False, indent=4)

  def save_csv(self, additional_path, data, file_name):
    save_path = os.path.join(self.data_path, additional_path)
    os.makedirs(save_path, exist_ok=True)
    output_file_path = os.path.join(save_path, f'{file_name}.csv')

    file_exists = os.path.isfile(output_file_path)
    mode = 'a' if file_exists else 'w'
    with open(output_file_path, mode, newline='', encoding='utf-8') as file:
      writer = csv.writer(file)
      if not file_exists:
        header = data.keys()
        writer.writerow(header)
      writer.writerow(data.values())

  def get_last_marine_data_timestamp(self, marine_data_path):
    files = os.listdir(marine_data_path)
    pattern = re.compile(r'fetched_data_\d{10}')
    matching_files = [file for file in files if pattern.match(file)]

    if not matching_files:
      return None

    last_timestamp = None

    matching_files.sort(key=lambda x: self._get_timestamp(x))

    last_file = matching_files[-1]
    if last_file:
      last_timestamp = self._get_timestamp(last_file)
    return last_timestamp

  def get_latest_json_and_timestamp(self, additional_path, data_type):
    files_path = os.path.join(self.data_path, additional_path)
    files = os.listdir(files_path)
    pattern = re.compile(data_type + r'_data_\d{10}')
    matching_files = [file for file in files if pattern.match(file)]

    if not matching_files:
      return None

    matching_files.sort(key=lambda x: self._get_timestamp(x, data_type))

    last_file = matching_files[-1]
    if last_file:
      file_path = os.path.join(files_path, last_file)
      with open(file_path, 'r') as file:
        return json.load(file) , self._get_timestamp(last_file, data_type)
    return None
  
  def get_dataframe(self, file_name, additional_path = ''):
    file_path = os.path.join(self.data_path, additional_path, f'{file_name}.csv')
    return pd.read_csv(file_path)