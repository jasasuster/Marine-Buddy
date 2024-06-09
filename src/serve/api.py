from flask import Flask, request
from flask_cors import CORS
from datetime import datetime

import os

from src.models.scripts.predict_model import predict
from src.models.mlflow_client import download_all_models, get_latest_model_metrics, get_production_metrics
from src.db.database_manager import DatabaseManager
from src.models.trained_model import get_classification_model, predict as predict_animal

def create_app(image_processor, image_model):
  app = Flask(__name__)
  database_manager = DatabaseManager()
  CORS(app)

  @app.route('/wave/<int:sea_point_number>', methods=['POST'])
  def predict_val(sea_point_number):
    try:
      if sea_point_number < 1 or sea_point_number > 10:
        return {'error': 'Invalid sea point number'}, 400
      predictions = predict(sea_point_number)
      database_manager.insert_prediction(f"sea_point_{sea_point_number}", {'predictions': predictions, 'date': datetime.now()})

      return {'predictions': predictions}, 200
    except Exception as e:
      return {'error': str(e)}, 400
    
  @app.route('/classification', methods=['POST'])
  def predict_classification():
    try:
      if 'image' not in request.files:
        return {'error': 'No image found in request'}, 400
      image = request.files['image']
      if image.filename == '':
        return {'error': 'No selected image'}, 400
      if image:
        prediction = predict_animal(image_processor, image_model, image)
        if prediction is None:
          return {'error': 'Error predicting image'}, 400
        
        if not os.path.isdir('predicted_images'):
          os.mkdir('predicted_images')
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        image.save(f"predicted_images/{prediction}_{timestamp}.jpg")

      return {'prediction': prediction}, 200
    except Exception as e:
      return {'error': str(e)}, 400
    
  @app.route('/evaluation', methods=['GET'])
  def get_evaluation():
    try:
      metrics = get_latest_model_metrics()
      return {'metrics': metrics}, 200
    except Exception as e:
      return {'error': str(e)}, 400
    
  @app.route('/production-evaluation', methods=['GET'])
  def get_production_evaluation():
    try:
      metrics = get_production_metrics()
      return {'metrics': metrics}, 200
    except Exception as e:
      return {'error': str(e)}, 400

  return app

def main():
  download_all_models()
  image_processor, image_model = get_classification_model()

  app = create_app(image_processor, image_model)

  app.run(host='0.0.0.0', port=3000)

if __name__ == '__main__':
  main()