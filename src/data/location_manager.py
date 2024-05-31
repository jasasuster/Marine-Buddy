import json

class LocationManager:
  def __init__(self):
    self.file_path = './locations.json'
    self.locations = self._load_locations()

  def _load_locations(self):
    with open(self.file_path) as file:
      locations = json.load(file)
    return locations
  
  def get_location_names(self):
    return [location['name'] for location in self.locations]
  
  def get_location_coordinates(self, sea_point_number):
    for location in self.locations:
      if location['name'] == f'Sea Point {sea_point_number}':
        return location['coordinates']['latitude'], location['coordinates']['longitude']
    return None

  def get_coordinates(self, location_name):
    for location in self.locations:
      if location['name'] == location_name:
        return location['coordinates']
    return None

  def get_all_coordinates(self):
    latitudes = [location['coordinates']['latitude'] for location in self.locations]
    longitudes = [location['coordinates']['longitude'] for location in self.locations]
    return latitudes, longitudes