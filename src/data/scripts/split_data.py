import os
import pandas as pd

def split_data(df):
  test_size = int(0.9 * len(df))
  train_df = df.head(test_size)
  test_df = df.iloc[test_size:]

  return train_df, test_df

def main():
  data_path = "data/processed/"
  for sea_point_number in range(1, 11):
    file_path = os.path.join(data_path, f"{sea_point_number}.csv")

    df = pd.read_csv(file_path)

    train_df, test_df = split_data(df)

    train_df.to_csv(f'data/processed/{sea_point_number}_train.csv', index=False)
    test_df.to_csv(f'data/processed/{sea_point_number}_test.csv', index=False)