# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 07:13:35 2023

@author: abiga
"""

import unittest
import pandas as pd
import dash_app


class TestApp(unittest.TestCase):

    def test_read_data_from_file(self):
        file_path = "../data/file_for_app_sample.pkl"
        data = dash_app.read_data_from_file(file_path)
        self.assertIsInstance(data, pd.DataFrame, "The returned object should be a pandas DataFrame.")

    def test_clean_df(self):
        raw_df = dash_app.read_data_from_file("../data/file_for_app_sample.pkl")
        cleaned_df = dash_app.clean_df(raw_df)

        self.assertIn("Close Date", cleaned_df.columns, "The 'Close Date' column should be present in the cleaned DataFrame.")
        self.assertEqual(cleaned_df["Min_salary"].dtype, 'int64', "The 'Min_salary' column should be of type 'int64'.")
        self.assertEqual(cleaned_df["Max_salary"].dtype, 'int64', "The 'Max_salary' column should be of type 'int64'.")

    def test_generate_tooltip_data(self):
        cleaned_df = dash_app.clean_df(dash_app.read_data_from_file("../data/file_for_app_sample.pkl"))
        tooltip_data = dash_app.generate_tooltip_data(cleaned_df)

        self.assertIsInstance(tooltip_data, list, "The returned object should be a list.")
        self.assertEqual(len(tooltip_data), len(cleaned_df), "The length of the tooltip data should be the same as the length of the cleaned DataFrame.")


if __name__ == '__main__':
    unittest.main()
