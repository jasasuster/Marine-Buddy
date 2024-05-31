from flask import Flask, request
from flask_cors import CORS
from datetime import datetime

from src.models.scripts.predict_model import predict
from src.models.mlflow_client import download_all_models
from src.db.database import insert_prediction

def create_app():
  app = Flask(__name__)
  CORS(app)

  @app.route('/mbajk/predict', methods=['POST'])
  def predict_val():
    try:
      data = request.get_json()
      station_number = data['station_number']
      print(station_number)
      predictions = predict(station_number)
      insert_prediction(f"station_{station_number}", {'predictions': predictions, 'date': datetime.now()})

      return {'predictions': predictions}, 200
    except Exception as e:
      return {'error': str(e)}, 400

  return app

def main():
  app = create_app()

  download_all_models()

  app.run(host='0.0.0.0', port=3000)

if __name__ == '__main__':
  main()