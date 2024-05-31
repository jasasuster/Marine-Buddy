import joblib
import pandas as pd
import onnxruntime as ort
from datetime import datetime, timedelta

from src.data.data_fetcher import DataFetcher
from src.data.location_manager import LocationManager
from src.models.model import prepare_predict_data

def hour_rounder(t):
  # Rounds to nearest hour by adding a timedelta hour if minute >= 30
  return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)+timedelta(hours=t.minute//30)).strftime('%Y-%m-%dT%H:%M')

def get_sea_point_data(sea_point_number):
  url = f"https://dagshub.com/jasasuster/Marine-Buddy/raw/main/data/processed/sea_point_{sea_point_number}.csv"
  df = pd.read_csv(url)
  return df 

def predict(sea_point_number):
  location_manager = LocationManager()
  coordinates = location_manager.get_all_coordinates()
  data_fetcher = DataFetcher(coordinates)

  sea_point_data = get_sea_point_data(sea_point_number)
  weather_data = data_fetcher.get_weather_data()

  rounded_time = hour_rounder(datetime.now(data_fetcher.timezone))
  index = weather_data['hourly']['time'].index(rounded_time)

  weather_df = pd.DataFrame()
  for i, row in weather_data.itterrows():
    hourly = row['hourly'][index + 1:index + 8]
    weather_df[row.name] = hourly

  models_dir = f"./models/{sea_point_number}"
  model = ort.InferenceSession(f"{models_dir}/model_production.onnx")
  wave_scaler = joblib.load(f"{models_dir}/wave_scaler.joblib")
  other_scaler = joblib.load(f"{models_dir}/other_scaler.joblib")

  predictions = []
  for i in range(7):
    X = prepare_predict_data(weather_df, wave_scaler, other_scaler)
    y_pred = model.run(["output"], {"input":X})[0]
    y_pred = wave_scaler.inverse_transform(y_pred).tolist()[0][0]
    predictions.append(y_pred)

    forecast_data = weather_df.iloc[i]
    forecast_data['wave_height'] = y_pred

    new_row_df = pd.DataFrame([forecast_data])
    sea_point_data = pd.concat([sea_point_data, new_row_df], ignore_index=True)
    sea_point_data = sea_point_data.iloc[1:]

  return predictions