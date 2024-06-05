from transformers import AutoImageProcessor, TFAutoModelForImageClassification
import tensorflow as tf
from PIL import Image

def get_classification_model():
  try:
    print("--------- Downloading pretrained model ---------")
    processor = AutoImageProcessor.from_pretrained("jasasuster/sea-animals")
    model = TFAutoModelForImageClassification.from_pretrained("jasasuster/sea-animals")
    print("Pretrained model downloaded successfully!")
    return processor, model
  except Exception as e:
    print(f"Error: {e}")

def preprocess_image(image, processor):
  print("--------- Preprocessing image ---------")
  try:
    image = Image.open(image).convert("RGB")
    inputs = processor(images=image, return_tensors="tf")
    return inputs["pixel_values"]
  except Exception as e:
    print(f"Error: {e}")
    return None

def predict(processor, model, image):
  print("--------- Predicting image ---------")
  try:
    preprocessed_image = preprocess_image(image, processor)
    output = model(preprocessed_image)
    predicted_class_idx = tf.argmax(output.logits, axis=1).numpy()[0]
    return model.config.id2label[predicted_class_idx]
  except Exception as e:
    print(f"Error: {e}")
    return None