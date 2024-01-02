import sys
import os

# Assuming the pipeline directory is a sibling of the unit_test directory
pipeline_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pipeline'))

# Add the pipeline directory to the Python path
sys.path.append(pipeline_path)

import unittest
from unittest.mock import patch
from pipeline.main import main

from pipeline.copy_tables import copy_table
from pipeline.data_quality_monitor import get_tables_and_columns, monitor_data_quality


class TestMainFunction(unittest.TestCase):
    @patch('builtins.print')  # Mock print function to avoid unwanted prints during testing
    @patch('copy_tables.copy_table')  # Correct path to the copy_table function
    def test_copy_tables(self, mock_copy_tables):
        main()
        mock_copy_tables.assert_called_once()

    @patch('builtins.print')  # Mock print function to avoid unwanted prints during testing
    @patch('data_quality_monitor.monitor_data_quality')  # Correct path to the monitor_data_quality function
    def test_monitor_data_quality(self, mock_monitor_data_quality):
        main()
        mock_monitor_data_quality.assert_called_once()

    def test_both_functions(self):
        with patch('copy_tables.copy_table') as mock_copy_tables, \
             patch('data_quality_monitor.monitor_data_quality') as mock_monitor_data_quality:
            main(scheduler_delay=0)
            mock_copy_tables.assert_called_once()
            mock_monitor_data_quality.assert_called_once()

            # If both functions pass, print success message
            print("Both tests worked!")

if __name__ == '__main__':
    unittest.main()
