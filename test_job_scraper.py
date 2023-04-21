import unittest
from unittest.mock import patch
import pandas as pd
import os

import job_scraper

class TestJobScraper(unittest.TestCase):

    def test_get_login(self):
        with patch('builtins.open', unittest.mock.mock_open(read_data='example_key')):
            directory = os.getcwd()
            authorization_key = job_scraper.get_login(directory)
            self.assertEqual(authorization_key, "example_key")

    def test_connect(self):
        headers = job_scraper.connect("example_key")
        expected_headers = {
            'Authorization-Key': 'example_key',
            'Host': 'data.usajobs.gov',
            'User-Agent': 'example@example.com'
        }
        self.assertEqual(headers, expected_headers)

    def test_current_search(self):
        with patch('job_scraper.requests.get') as mock_get:
            mock_get.return_value.json.return_value = {
                'SearchResult': {'SearchResultItems': []}
            }
            result = job_scraper.current_search("example_key", "Organization_Code")
            self.assertIsInstance(result, pd.DataFrame)

    def test_get_agencies(self):
        with patch('job_scraper.requests.get') as mock_get:
            mock_get.return_value.json.return_value = {
                'CodeList': [
                    {
                        'ValidValue': [
                            {'Code': 'A', 'IsDisabled': 'No'},
                            {'Code': 'B', 'IsDisabled': 'Yes'},
                        ]
                    }
                ]
            }
            result = job_scraper.get_agencies()
            self.assertIsInstance(result, pd.DataFrame)
            self.assertTrue((result['IsDisabled'] == 'No').all())

    def test_search_all_agencies_current(self):
        with patch('job_scraper.get_agencies') as mock_get_agencies, \
             patch('job_scraper.current_search') as mock_current_search, \
             patch('job_scraper.get_login') as mock_get_login:
            mock_get_agencies.return_value = pd.DataFrame([{'Code': 'A'}])
            mock_current_search.return_value = pd.DataFrame()
            mock_get_login.return_value = "example_key"
            result = job_scraper.search_all_agencies_current()
            self.assertIsInstance(result, pd.DataFrame)

    def test_main(self):
        with patch('job_scraper.search_all_agencies_current') as mock_search_all_agencies_current:
            mock_search_all_agencies_current.return_value = pd.DataFrame()
            result = job_scraper.main()
            self.assertIsInstance(result, pd.DataFrame)
            
class TestUnpackColumnDict(unittest.TestCase):

    def test_unpack_column_dict(self):
        data_frame = pd.DataFrame({
            'A': [1, 2],
            'B': [{'x': 10, 'y': 20}, {'x': 30, 'y': 40}]
        })
        result = job_scraper.unpack_column_dict(data_frame, 'B')
        expected_result = pd.DataFrame({
            'A': [1, 2],
            'x': [10, 30],
            'y': [20, 40]
        })
        self.assertTrue(result.equals(expected_result))

    def test_unpack_column_dict_no_dict(self):
        data_frame = pd.DataFrame({
            'A': [1, 2],
            'B': [3, 4]
        })
        result = job_scraper.unpack_column_dict(data_frame, 'B')
        self.assertTrue(result.equals(data_frame))


    def test_pull_fields_from_dict_no_dict(self):
        data_frame = pd.DataFrame({
            'A': [1, 2],
            'B': [3, 4],
            'C': [5, 6]
        })
        result = job_scraper.pull_fields_from_dict(data_frame)
        self.assertTrue(result.equals(data_frame))
    def test_pull_fields_from_dict(self):
        data_frame = pd.DataFrame({
        'A': [1, 2],
        'B': [{'x': 10, 'y': 20}, {'x': 30, 'y': 40}],
        'C': [{'z': 100}, {'z': 200}]
    })
        result = job_scraper.pull_fields_from_dict(data_frame)
        expected_result = pd.DataFrame({
        'A': [1, 2],
        'x': [10, 30],
        'y': [20, 40],
        'z': [100, 200]
        }) # Add this line to print the resulting DataFrame
        self.assertTrue(result.equals(expected_result))


if __name__ == "__main__":
    unittest.main()
