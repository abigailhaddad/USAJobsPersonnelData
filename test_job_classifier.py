import unittest
import pandas as pd

import job_classifier

class TestFunctions(unittest.TestCase):
    def test_add_leading_zero(self):
        self.assertEqual(job_classifier.add_leading_zero("123"), "0123")
        self.assertEqual(job_classifier.add_leading_zero("0123"), "0123")
        self.assertEqual(job_classifier.add_leading_zero("001"), "0001")

    def test_concatenate_columns(self):
        data = {'col1': [1, 2], 'col2': [3, 4], 'col3': [5, 6]}
        df = pd.DataFrame(data)
        expected_data = {'col1': [1, 2], 'col2': [3, 4], 'col3': [5, 6], 'info': ['1 3 5', '2 4 6']}
        expected_df = pd.DataFrame(expected_data)
        result_df = job_classifier.concatenate_columns(df, ['col1', 'col2', 'col3'], 'info')
        self.assertTrue(result_df.equals(expected_df))


    def test_extract_min_max(self):
        salary_list = [{'MinimumRange': 50000, 'MaximumRange': 100000}]
        self.assertEqual(job_classifier.extract_min_max(salary_list), (50000, 100000))
        self.assertEqual(job_classifier.extract_min_max([]), (None, None))

    def test_extract_location_names(self):
        location_list = [{'LocationName': 'New York, NY'}, {'LocationName': 'San Francisco, CA'}]
        self.assertEqual(job_classifier.extract_location_names(location_list), 'New York, NY; San Francisco, CA')

if __name__ == '__main__':
    unittest.main()
