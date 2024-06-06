import mlflow
import dagshub
import pandas as pd

from datetime import timedelta
from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score

from src.db.database_manager import DatabaseManager
import src.settings as settings

def test_predictions(station_number, sea_point_data, database_manager):
  sea_point_predictions = database_manager.predictions_today(f"sea_point_{station_number}")

  if not sea_point_predictions:
    print(f"No predictions for today for sea point {station_number}")
    mlflow.end_run()
    return
  
  mlflow.start_run(run_name=f"sea_point_{station_number}", experiment_id=2)

  mapped_predictions = []
  for prediction in sea_point_predictions:
    predictions_hourly = prediction['predictions']
    date = pd.to_datetime(prediction['date'])
    sea_point_data.reset_index(inplace=True)
    sea_point_data = sea_point_data.set_index('timestamp')
    for i, pred in enumerate(predictions_hourly):
      target_time = date + timedelta(hours=i)
      nearest_timestamp_index = sea_point_data.index.get_indexer([target_time], method='nearest')[0]
      nearest_timestamp_sea_data = sea_point_data.iloc[nearest_timestamp_index].to_dict()
      mapped_predictions.append({
        'date': target_time,
        'prediction': pred,
        'true': nearest_timestamp_sea_data['wave_height']
      })

  y_true = [pred['true'] for pred in mapped_predictions]
  y_pred = [pred['prediction'] for pred in mapped_predictions]

  mse = mean_squared_error(y_true, y_pred)
  mae = mean_absolute_error(y_true, y_pred)
  evs = explained_variance_score(y_true, y_pred)

  mlflow.log_metric('mse', mse)
  mlflow.log_metric('mae', mae)
  mlflow.log_metric('evs', evs)

  mlflow.end_run()

def main():
  database_manager = DatabaseManager()
  dagshub.auth.add_app_token(token=settings.MLFLOW_TRACKING_PASSWORD)
  dagshub.init("Marine-Buddy", settings.MLFLOW_TRACKING_USERNAME, mlflow=True)
  mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

  for sea_point_number in range(1, 11):
    print(f"---------- Testing sea point {sea_point_number} ----------")
    sea_point_data = pd.read_csv(f"./data/processed/{sea_point_number}.csv")
    sea_point_data.sort_values(by='timestamp', inplace=True)
    sea_point_data.drop_duplicates(subset='timestamp', inplace=True)
    sea_point_data.reset_index(inplace=True)
    sea_point_data.set_index('timestamp')

    test_predictions(sea_point_number, sea_point_data, database_manager)

if __name__ == '__main__':
  main()