import numpy as np
import pandas as pd

from tensorflow.keras import Input
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense, Dropout
from tensorflow_model_optimization.quantization.keras import quantize_annotate_layer, quantize_apply

import src.settings as settings
from src.data.data_manager import DataManager
from src.visualization.visualization import plot_model_history

def build_model(input_shape):
  model = Sequential()

  model.add(Input(shape=input_shape))
  model.add(GRU(128, return_sequences=True))
  model.add(Dropout(0.2))

  model.add(GRU(64, return_sequences=True))
  model.add(Dropout(0.2))

  model.add(GRU(32, activation='relu'))

  model.add(quantize_annotate_layer(Dense(32, activation='relu')))
  model.add(quantize_annotate_layer(Dense(1)))

  model = quantize_apply(model)

  model.compile(optimizer='adam', loss='mse')

  return model

def train_model(model, sea_point_number, X_train, y_train, epochs, batch_size=32):
  model_history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2, verbose=1)
  plot_model_history(model_history, sea_point_number)

def get_data(sea_point_number, data_type):
  data_manager = DataManager('data/processed/')
  df = data_manager.get_dataframe(f"sea_point_{sea_point_number}_{data_type}")
  return df

def scale_data(train, test, wave_scaler, other_scaler):
  train_wave, test_wave = np.array(train[:,0]), np.array(test[:,0])
  train_other, test_other = np.array(train[:,1:]), np.array(test[:,1:])

  train_wave = wave_scaler.fit_transform(train_wave.reshape(-1, 1))
  test_wave = wave_scaler.transform(test_wave.reshape(-1, 1))

  train_other = other_scaler.fit_transform(train_other)
  test_other = other_scaler.transform(test_other)

  train_scaled = np.column_stack([train_wave, train_other])
  test_scaled = np.column_stack([test_wave, test_other])

  return train_scaled, test_scaled

def create_time_series(df, window_size=5):
  X, y = [], []
  for i in range(len(df) - window_size):
      window = df[i:i+window_size, :]
      target = df[i+window_size, 0]
      X.append(window)
      y.append(target)
  return np.array(X), np.array(y)

def prepare_data(df, wave_scaler, other_scaler):
  df = df.sort_values(by='timestamp')
  df.set_index('timestamp', inplace=True)
  df.reset_index(inplace=True)
  df.dropna(inplace=True)

  df_multi = df[['wave_height','temperature_2m','wind_speed_10m','wind_direction_10m','relative_humidity_2m','dew_point_2m','apparent_temperature','precipitation_probability','rain','surface_pressure']]
  multi_array = df_multi.values

  train_size = len(multi_array) - (len(multi_array) // 5)
  train, test = multi_array[:train_size], multi_array[train_size:]

  train_scaled, test_scaled = scale_data(train, test, wave_scaler, other_scaler)
  X_train, y_train = create_time_series(train_scaled, settings.window_size)
  X_test, y_test = create_time_series(test_scaled, settings.window_size)

  X_train = X_train.reshape(X_train.shape[0], train_scaled.shape[1], X_train.shape[1])
  X_test = X_test.reshape(X_test.shape[0], test_scaled.shape[1], X_test.shape[1])

  return X_train, y_train, X_test, y_test

def prepare_evaluate_data(df, wave_scaler, other_scaler):
  df = df.sort_values(by='timestamp')
  df.set_index('timestamp', inplace=True)
  df.reset_index(inplace=True)
  df.dropna(inplace=True)

  df_multi = df[['wave_height','temperature_2m','wind_speed_10m','wind_direction_10m','relative_humidity_2m','dew_point_2m','apparent_temperature','precipitation_probability','rain','surface_pressure']]
  multi_array = df_multi.values

  target_feature = multi_array[:,0]
  target_feature_normalized = wave_scaler.transform(target_feature.reshape(-1, 1))

  other_features = multi_array[:,1:]
  other_features_normalized = other_scaler.transform(other_features)

  multi_array_scaled = np.column_stack([target_feature_normalized, other_features_normalized])

  X_final, y_final = create_time_series(multi_array_scaled, settings.window_size)

  X_final = X_final.reshape(X_final.shape[0], multi_array_scaled.shape[1], X_final.shape[1])

  return X_final, y_final

def prepare_predict_data(df, wave_scaler, other_scaler):
  df = df.sort_values(by='timestamp')

  df_multi = df[['wave_height', 'temperature_2m','wind_speed_10m','wind_direction_10m','relative_humidity_2m','dew_point_2m','apparent_temperature','precipitation_probability','rain','surface_pressure']]
  multi_array = df_multi.values

  wave_feature = multi_array[:,0]
  other_features = multi_array[:,1:]

  wave_feature = wave_scaler.transform(wave_feature.reshape(-1, 1))
  other_features = other_scaler.transform(other_features)

  multi_array = np.column_stack([wave_feature, other_features])
  multi_array = multi_array.reshape(1, multi_array.shape[1], multi_array.shape[0])

  return multi_array