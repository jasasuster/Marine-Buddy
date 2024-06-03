from huggingface_hub import from_pretrained_keras

def download_and_save_pretrained_model():
  try:
    model = from_pretrained_keras("eljapo/sea-animal")
    print("Pretrained model downloaded successfully!")
    print(model.summary())
    model.save("models/classification/trained_model.h5")
  except Exception as e:
    print(f"Error: {e}")

def predict():
  pass