import matplotlib.pyplot as plt
import os

def plot_model_history(history, sea_point_number):
  plt.plot(history.history['loss'], label='Train Loss')
  plt.plot(history.history['val_loss'], label='Validation Loss')
  plt.title(f'Model {sea_point_number} Learning History')
  plt.xlabel('Epochs')
  plt.ylabel('Loss')
  plt.legend()
  plt.tight_layout()
  save_path = "./reports/figures"
  os.makedirs(save_path, exist_ok=True)
  plt.savefig(os.path.join(save_path, f"model_{sea_point_number}_history.png"))
  plt.close()