import mlflow
import dagshub
import tf2onnx
import tensorflow as tf

from mlflow import MlflowClient
from mlflow.models import infer_signature
from sklearn.preprocessing import MinMaxScaler
from mlflow.onnx import log_model as log_onnx_model
from mlflow.sklearn import log_model as log_sklearn_model

import src.settings as settings
from src.models.model import get_data, prepare_data, build_model, train_model

def mlflow_save_scaler(client, scaler_type, scaler, sea_point_number):
  metadata = {
    "station_name": sea_point_number,
    "scaler_type": scaler_type,
  }

  scaler = log_sklearn_model(
    sk_model=scaler,
    artifact_path=f"models/{sea_point_number}/{scaler_type}",
    registered_model_name=f"{scaler_type}_{sea_point_number}",
    metadata=metadata,
  )

  scaler_version = client.create_model_version(
    name=f"{scaler_type}_{sea_point_number}",
    source=scaler.model_uri,
    run_id=scaler.run_id
  )

  client.transition_model_version_stage(
    name=f"{scaler_type}_{sea_point_number}",
    version=scaler_version.version,
    stage="staging",
  )

def mlflow_save_onnx(client, model, feature_number, window_size, sea_point_number, X_test):
  model.output_names = ["output"]

  input_signature = [
    tf.TensorSpec(shape=(None, window_size, feature_number), dtype=tf.double, name="input")
  ]

  onnx_model, _ = tf2onnx.convert.from_keras(model=model, input_signature=input_signature, opset=13)

  model_ = log_onnx_model(
    onnx_model=onnx_model, 
    artifact_path=f"models/{sea_point_number}/model", 
    signature=infer_signature(X_test, model.predict(X_test)), 
    registered_model_name=f"model_{sea_point_number}"
  )

  mv = client.create_model_version(name=f"model_{sea_point_number}", source=model_.model_uri, run_id=model_.run_id)

  client.transition_model_version_stage(name=f"model_{sea_point_number}", version=mv.version, stage="staging")

def train(sea_point_number):
  client = MlflowClient()

  mlflow.start_run(run_name=f"sea_point_{sea_point_number}", experiment_id=0)
  mlflow.tensorflow.autolog()

  data = get_data(sea_point_number, "train")
  wave_scaler = MinMaxScaler()
  other_scaler = MinMaxScaler()
  X_train, y_train, X_test, y_test = prepare_data(data, wave_scaler, other_scaler)

  input_shape = (X_train.shape[1], X_train.shape[2])
  model = build_model(input_shape)

  epochs = 15
  batch_size = 32

  train_model(model, X_train, y_train, epochs, batch_size)

  mlflow.log_param("epochs", 15)
  mlflow.log_param("batch_size", 32)
  mlflow.log_param("train_dataset_size", len(X_train))

  mlflow_save_scaler(client, "wave_scaler", wave_scaler, sea_point_number)
  mlflow_save_scaler(client, "other_scaler", other_scaler, sea_point_number)

  mlflow_save_onnx(client, model, X_train.shape[2], X_train.shape[1], sea_point_number, X_test)

  mlflow.end_run()

def main():
  dagshub.auth.add_app_token(token=settings.MLFLOW_TRACKING_PASSWORD)
  dagshub.init("Marine-Buddy", settings.MLFLOW_TRACKING_USERNAME, mlflow=True)
  mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)

  for sea_point_number in range(1, 10):
    train(sea_point_number)