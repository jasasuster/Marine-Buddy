import os
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

def main():
  report = Report(metrics=[DataDriftPreset()])

  current_path = os.path.join('data', 'processed', 'current_data.csv')
  reference_path = os.path.join('data', 'processed', 'sea_point_1.csv')

  current = pd.read_csv(current_path)
  reference = pd.read_csv(reference_path)

  report.run(reference_data=reference, current_data=current)

  report.save_html("reports/sites/data_drift.html")