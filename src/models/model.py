import numpy as np

from tensorflow.keras import Input
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense, Dropout
from tensorflow_model_optimization.quantization.keras import quantize_annotate_layer, quantize_apply

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

def train_model(model, X_train, y_train, epochs, batch_size=32):
  model_history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2, verbose=1)
  plot_model_history(model_history)

def evaluate_model():
  pass

def get_data(sea_point_number, data_type):
  data_manager = DataManager('data/processed/')
  df = data_manager.get_dataframe(f"sea_point_{sea_point_number}_{data_type}")
  return df

def scale_data(train, test, wave_scaler, other_scaler):
  train_wave, test_wave = train['wave_height'].values, test['wave_height'].values
  train_other, test_other = train.drop(columns=['wave_height']).values, test.drop(columns=['wave_height']).values

  train_wave = wave_scaler.fit_transform(train_wave.reshape(-1, 1))
  test_wave = wave_scaler.transform(test_wave.reshape(-1, 1))

  train_other = other_scaler.fit_transform(train_other)
  test_other = other_scaler.transform(test_other)

  train_scaled = np.column_stack([train_wave, train_other])
  test_scaled = np.column_stack([test_wave, test_other])

  return train_scaled, test_scaled

def create_time_series(df, window_size=24):
  X, y = [], []
  for i in range(len(df) - window_size):
      window = df[i:i+window_size, :]
      target = df[i+window_size, 0]
      X.append(window)
      y.append(target)
  return np.array(X), np.array(y)

def prepare_data(df, wave_scaler, other_scaler):
  df.drop(columns=['latitude', 'longitude', 'elevation', 'location_id', 'location_name'], inplace=True)
  # df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
  # df.drop(columns=['timestamp'], inplace=True)
  df.set_index('timestamp', inplace=True)
  df = df.resample('h').mean()
  df.reset_index(inplace=True)
  df.dropna(inplace=True)

  train_size = len(df) - (len(df) // 5)
  train, test = df[:train_size], df[train_size:]

  train_scaled, test_scaled = scale_data(train, test, wave_scaler, other_scaler)
  X_train, y_train = create_time_series(train_scaled)
  X_test, y_test = create_time_series(test_scaled)

  X_train = X_train.reshape(X_train.shape[0], train_scaled.shape[1], X_train.shape[1])
  X_test = X_test.reshape(X_test.shape[0], test_scaled.shape[1], X_test.shape[1])

  return X_train, y_train, X_test, y_test