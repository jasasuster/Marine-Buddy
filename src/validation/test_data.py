import sys
import os
import pandas as pd
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

from evidently.test_suite import TestSuite
from evidently.tests import TestNumberOfColumnsWithMissingValues, TestNumberOfRowsWithMissingValues, \
  TestNumberOfConstantColumns, TestNumberOfDuplicatedRows, TestNumberOfDuplicatedColumns, TestColumnsType, \
  TestNumberOfDriftedColumns

def main():
  tests = TestSuite(tests=[
    TestNumberOfColumnsWithMissingValues(),
    TestNumberOfRowsWithMissingValues(),
    TestNumberOfConstantColumns(),
    TestNumberOfDuplicatedRows(),
    TestNumberOfDuplicatedColumns(),
    TestColumnsType(),
    TestNumberOfDriftedColumns()
  ])

  current_path = os.path.join('data', 'processed', 'current_data.csv')
  reference_path = os.path.join('data', 'processed', 'sea_point_1.csv')

  current = pd.read_csv(current_path)
  reference = pd.read_csv(reference_path)

  tests.run(reference_data=reference, current_data=current)

  tests.save_html("reports/sites/index.html")

  test_results = tests.as_dict()

  # Check if any test failed
  # if test_results['summary']['failed_tests'] > 0:
  #   print("Some tests failed:")
  #   print(test_results['summary']['failed_tests'])
  #   sys.exit(1)
  # else:
  #   print("All tests passed!")