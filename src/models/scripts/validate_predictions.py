import os
import mlflow
import dagshub
import onnxruntime 
import dagshub.auth
import pandas as pd

from sklearn.metrics import mean_absolute_error, mean_squared_error, explained_variance_score

import src.settings as settings
import src.models.mlflow_client as mlflow_client
from src.models.model import get_data, prepare_predict_data

def evaluate_model(sea_point_number):
  with mlflow.start_run(run_name=f"sea_point_{sea_point_number}", experiment_id="1", nested=True):
    mlflow.tensorflow.autolog()

    model = mlflow_client.download_latest_model_onnx(sea_point_number, "staging")
    loaded_wave_scaler = mlflow_client.download_latest_scaler(sea_point_number, "wave_scaler", "staging")
    loaded_other_scaler = mlflow_client.download_latest_scaler(sea_point_number, "other_scaler", "staging")

    production_model = mlflow_client.download_latest_model_onnx(sea_point_number, "production")
    production_wave_scaler = mlflow_client.download_latest_scaler(sea_point_number, "wave_scaler", "production")
    production_other_scaler = mlflow_client.download_latest_scaler(sea_point_number, "other_scaler", "production")

    if model is None or loaded_wave_scaler is None or loaded_other_scaler is None:
      print("Error loading model or scalers")
      mlflow.end_run()
      return
    
    if production_model is None or production_wave_scaler is None or production_other_scaler is None:
      print("Production model or scalers not found, replacing with latest staging model and scalers")
      mlflow_client.save_production_model_and_scalers(sea_point_number)
      mlflow.end_run()
      return

    print("Model and scalers loaded")

    model = onnxruntime.InferenceSession(model)
    production_model = onnxruntime.InferenceSession(production_model)

    df = get_data(sea_point_number, "test")

    X_final, y_final = prepare_predict_data(df, loaded_wave_scaler, loaded_other_scaler)
    production_X_final, production_y_final = prepare_predict_data(df, production_wave_scaler, production_other_scaler)

    y_pred = model.run(["output"], {"input":X_final})[0]
    y_test = loaded_wave_scaler.inverse_transform(y_final.reshape(-1, 1)).flatten()
    y_pred = loaded_wave_scaler.inverse_transform(y_pred)

    production_y_pred = production_model.run(["output"], {"input":production_X_final})[0]
    production_y_test = production_wave_scaler.inverse_transform(production_y_final.reshape(-1, 1)).flatten()
    production_y_pred = production_wave_scaler.inverse_transform(production_y_pred)

    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    evs = explained_variance_score(y_test, y_pred)
    print(f"MAE: {mae}, MSE: {mse}, EVS: {evs}")

    production_mae = mean_absolute_error(production_y_test, production_y_pred)
    production_mse = mean_squared_error(production_y_test, production_y_pred)
    production_evs = explained_variance_score(production_y_test, production_y_pred)
    print(f"Production MAE: {production_mae}, MSE: {production_mse}, EVS: {production_evs}")

    mlflow.log_metric("MAE staging", mae)
    mlflow.log_metric("MSE staging", mse)
    mlflow.log_metric("EVS staging", evs)

    mlflow.log_metric("MAE production", production_mae)
    mlflow.log_metric("MSE production", production_mse)
    mlflow.log_metric("EVS production", production_evs)

    # Save
    test_metrics = pd.DataFrame({
      'mae': [mae],
      'mse': [mse],
      'evs': [evs]
    })
    os.makedirs(f'./reports/sea_point_{sea_point_number}', exist_ok=True)
    test_metrics.to_csv(f'./reports/sea_point_{sea_point_number}/test_metrics.txt', sep='\t', index=False)

    if mae < production_mae and mse < production_mse and evs > production_evs:
      print("Production model is better, replacing with staging model")
      mlflow_client.save_production_model_and_scalers(sea_point_number)
    
    mlflow.end_run()

def main():
  dagshub.auth.add_app_token(token=settings.MLFLOW_TRACKING_PASSWORD)
  dagshub.init("Marine-Buddy", settings.MLFLOW_TRACKING_USERNAME, mlflow=True)
  mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

  for sea_point_number in range(1, 11):
    print(f"Evaluating model for sea point {sea_point_number}...")
    evaluate_model(sea_point_number)

if __name__ == '__main__':
  main()