import os
import onnx
import joblib
import mlflow
import dagshub
import pandas as pd
import src.settings as settings

from mlflow.onnx import load_model as load_onnx
from mlflow.sklearn import load_model as load_sklearn

def download_latest_model_onnx(sea_point_number, stage):
  model_name = f"model_{sea_point_number}"

  try:
    client = mlflow.MlflowClient()
    model = load_onnx( client.get_latest_versions(name=model_name, stages=[stage])[0].source)

    model_save_path = f"./models/{sea_point_number}/"
    os.makedirs(model_save_path, exist_ok=True)

    saved_model_path = f"./models/{sea_point_number}/model_{stage}.onnx"
    onnx.save_model(model, saved_model_path)

    return saved_model_path
  except IndexError:
    print(f"Error downloading {stage}, {model_name}")
    return None
  
def download_latest_scaler(sea_point_number, scaler_type, stage):
  scaler_name = f"{scaler_type}_{sea_point_number}"

  try:
    client = mlflow.MlflowClient()
    scaler = load_sklearn(client.get_latest_versions(name=scaler_name, stages=[stage])[0].source)
    return scaler
  except IndexError:
    print(f"Error downloading {stage}, {scaler_name}")
    return None

def save_production_model_and_scalers(sea_point_number):
  try:
    client = mlflow.MlflowClient()

    model_version = client.get_latest_versions(name= f"model_{sea_point_number}", stages=["staging"])[0].version
    client.transition_model_version_stage(f"model_{sea_point_number}", model_version, "production")

    wave_scaler_version = client.get_latest_versions(name=f"wave_scaler_{sea_point_number}", stages=["staging"])[0].version
    client.transition_model_version_stage(f"wave_scaler_{sea_point_number}", wave_scaler_version, "production")
    
    other_scaler_version = client.get_latest_versions(name= f"other_scaler_{sea_point_number}", stages=["staging"])[0].version
    client.transition_model_version_stage(f"other_scaler_{sea_point_number}", other_scaler_version, "production")

  except IndexError:
    print(f"#####error##### \n replace_prod_model {sea_point_number}")
    return

def download_all_models():
  dagshub.auth.add_app_token(token=settings.MLFLOW_TRACKING_PASSWORD)
  dagshub.init("Marine-Buddy", settings.MLFLOW_TRACKING_USERNAME, mlflow=True)
  mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

  try:
    for i in range(1, 11):
      print(f"------------------- downloading model and scalers for point {i} -------------------")
      sea_point_dir = f"models/{i}/"
      os.makedirs(sea_point_dir, exist_ok=True)
      model = download_latest_model_onnx(str(i), "production")
      print(f"model for point {i} downloaded")
      wave_scaler = download_latest_scaler(str(i), "wave_scaler", "production")
      print(f"wave scaler for point {i} downloaded")
      other_scaler = download_latest_scaler(str(i), "other_scaler", "production")
      print(f"other scaler for point {i} downloaded")

      joblib.dump(wave_scaler, os.path.join(sea_point_dir, 'wave_scaler.joblib'))
      joblib.dump(other_scaler, os.path.join(sea_point_dir, 'other_scaler.joblib'))

  except IndexError as e:
    print("Error getting models:", e)
    return None
  
def get_latest_model_metrics():
  try:
    client = mlflow.tracking.MlflowClient()
    experiment_id = "1"
    runs = client.search_runs(experiment_ids=experiment_id, filter_string="tags.`mlflow.runName` = 'sea_point_1'", order_by=["attributes.end_time desc"])
    metrics_data_list = []

    for run in runs:
      metrics = run.data.metrics
      if all([
        metrics.get("EVS production") is not None,
        metrics.get("MAE production") is not None,
        metrics.get("MSE production") is not None,
        metrics.get("EVS staging") is not None,
        metrics.get("MAE staging") is not None,
        metrics.get("MSE staging") is not None
      ]):
        metrics_data_list.append({
          "run_id": run.info.run_id,
          "end_time": pd.to_datetime(run.info.end_time, unit='ms').isoformat(),
          "EVS_production": metrics.get("EVS production"),
          "MAE_production": metrics.get("MAE production"),
          "MSE_production": metrics.get("MSE production"),
          "EVS_staging": metrics.get("EVS staging"),
          "MAE_staging": metrics.get("MAE staging"),
          "MSE_staging": metrics.get("MSE staging")
        })

    return metrics_data_list
  except IndexError:
    print("Error getting evaluation")
    return None
  
def get_production_metrics():
  try:
    client = mlflow.tracking.MlflowClient()
    experiment_id = "2"
    runs = client.search_runs(experiment_ids=experiment_id, filter_string="tags.`mlflow.runName` = 'sea_point_1'", order_by=["attributes.end_time desc"])
    metrics_data_list = []

    for run in runs:
      metrics = run.data.metrics
      if all([
        metrics.get("mse") is not None,
        metrics.get("evs") is not None,
        metrics.get("mae") is not None
      ]):
        metrics_data_list.append({
          "run_id": run.info.run_id,
          "end_time": pd.to_datetime(run.info.end_time, unit='ms').isoformat(),
          "mse": metrics.get("mse"),
          "evs": metrics.get("evs"),
          "mae": metrics.get("mae")
        })

    return metrics_data_list
  except IndexError:
    print("Error getting evaluation")
    return None