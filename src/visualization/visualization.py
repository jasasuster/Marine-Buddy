import matplotlib.pyplot as plt
import os

def plot_model_history(history):
  plt.plot(history.history['loss'], label='Train Loss')
  plt.plot(history.history['val_loss'], label='Validation Loss')
  plt.title('Model Learning History')
  plt.xlabel('Epochs')
  plt.ylabel('Loss')
  plt.legend()
  plt.tight_layout()
  save_path = "./reports/figures"
  os.makedirs(save_path, exist_ok=True)
  plt.savefig(os.path.join(save_path, "model_history.png"))
  plt.close()