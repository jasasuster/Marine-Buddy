import os
import onnx
import joblib
import mlflow
import dagshub
import src.settings as settings

from mlflow.onnx import load_model as load_onnx
from mlflow.sklearn import load_model as load_sklearn

def download_latest_model_onnx(sea_point_number, stage):
  model_name = f"model_{sea_point_number}"

  try:
    client = mlflow.MlflowClient()
    model = load_onnx( client.get_latest_versions(name=model_name, stages=[stage])[0].source)

    onnx.save_model(model, f"./models/{sea_point_number}/model_{stage}.onnx")

    return f"./models/{sea_point_number}/model_{stage}.onnx"
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
        sea_point_dir = f"models/{i}/"
        os.makedirs(sea_point_dir, exist_ok=True)
        model = download_latest_model_onnx(str(i), "production")
        wave_scaler = download_latest_scaler(str(i), "wave_scaler", "production")
        other_scaler = download_latest_scaler(str(i), "other_scaler", "production")

        joblib.dump(wave_scaler, os.path.join(sea_point_dir, 'wave_scaler.joblib'))
        joblib.dump(other_scaler, os.path.join(sea_point_dir, 'other_scaler.joblib'))

  except:
    print("Error getting models")
    return None