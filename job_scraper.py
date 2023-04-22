"""
A script to fetch current job data from the USAJobs API and save it to a file.
"""


import os
from typing import Dict
import requests
import pandas as pd

def get_login(directory: str) -> str:
    """
    Get the authorization key from a text file.

    Args:
        directory (str): The directory containing the key file.

    Returns:
        str: The authorization key.
    """
    file_loc="key/authorization_key.txt"
    with open(directory.replace("code", file_loc), "r", encoding="utf-8") as file:
        authorization_key = file.read()
    return authorization_key


def connect(authorization_key: str) -> Dict[str, str]:
    """
    Pass the key to the API.

    Args:
        authorization_key (str): The API authorization key.

    Returns:
        dict: The headers required for making requests to the API.
    """
    headers = {
        'Authorization-Key': authorization_key,
        'Host': 'data.usajobs.gov',
        'User-Agent': 'example@example.com'
    }
    return headers


def current_search(authorization_key: str, organization: str = "") -> pd.DataFrame:
    """
    Fetch current jobs data from the API and return it as a DataFrame.

    Args:
        authorization_key (str): The API authorization key.
        organization (str, optional): The organization code. Defaults to an empty string.

    Returns:
        pd.DataFrame: A DataFrame containing the fetched job data.
    """
    number = "0"
    base_url = f"https://data.usajobs.gov/api/Search?Organization={organization}&p={number}"
    results = requests.get(base_url, headers=connect(authorization_key), timeout=10).json()
    search_result_df = pd.DataFrame.from_dict(results['SearchResult']['SearchResultItems'])
    if len(search_result_df) == 25:
        while results['SearchResult']['SearchResultCount'] != 0:
            number = str(int(number) + 1)
            headers=connect(authorization_key)
            results = requests.get(base_url + number, headers=headers, timeout=10).json()
            new_df = pd.DataFrame.from_dict(results['SearchResult']['SearchResultItems'])
            search_result_df = pd.concat([search_result_df, new_df])
    return search_result_df


def get_agencies() -> pd.DataFrame:
    """
    Fetch a list of active agencies from the API.

    Returns:
        pd.DataFrame: A DataFrame containing the list of active agencies.
    """
    base_url = 'https://data.usajobs.gov/api/codelist/agencysubelements'
    results = requests.get(base_url, timeout=10).json()
    agencies = pd.DataFrame(results['CodeList'][0]['ValidValue'])
    active_agencies = agencies.loc[agencies['IsDisabled'] == "No"]
    return active_agencies


def search_all_agencies_current() -> pd.DataFrame:
    """
    Fetch current job data for all active agencies and return it as a DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the fetched job data.
    """
    directory = os.getcwd()
    authorization_key = get_login(directory)
    agencies = get_agencies()
    codes = list(agencies['Code'])
    data_frames = [current_search(authorization_key, organization=i) for i in codes]
    all_df = pd.concat(data_frames, axis=0)
    return all_df

def unpack_column_dict(data_frame: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Unpacks the specified column of a DataFrame if it contains dictionaries.

    Args:
        data_frame (pd.DataFrame): The input DataFrame.
        column (str): The column name to be unpacked.

    Returns:
        pd.DataFrame: A DataFrame with the specified column unpacked if it contained dictionaries.
                      Otherwise, the original DataFrame is returned.
    """
    new_columns = data_frame[column].apply(pd.Series)
    if len(new_columns.columns) > 1:
        new_data_frame = pd.concat([data_frame.drop(columns=[column]), new_columns], axis=1)
        return new_data_frame
    return data_frame

def pull_fields_from_dict(data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Recursively unpacks all columns in a DataFrame containing dictionaries.

    Args:
        data_frame (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: A DataFrame with all columns containing dictionaries unpacked.
    """
    data_frame_changed = True
    while data_frame_changed:
        data_frame_changed = False
        columns_to_remove = []
        new_columns = []

        for column in data_frame.columns:
            if dict in [type(item) for item in data_frame[column].values]:
                data_frame_changed = True
                new_columns.append(data_frame[column].apply(pd.Series))
                columns_to_remove.append(column)

        if data_frame_changed:
            data_frame = data_frame.drop(columns=columns_to_remove)
            data_frame = pd.concat([data_frame, *new_columns], axis=1)
            data_frame = data_frame.dropna(how='all', axis=1)

    return data_frame



def main() -> pd.DataFrame:
    """
    Run a new current jobs search for all active agencies and return the data as a DataFrame.

    Returns:
        pd.DataFrame: A DataFrame containing the fetched job data.
    """
    current_data = search_all_agencies_current()
    current_data_unpacked=pull_fields_from_dict(current_data)
    current_data_unpacked.to_pickle("../data/currentResults.pkl")
    return current_data_unpacked


if __name__ == "__main__":
    current_data_from_function = main()   
    print(current_data_from_function.head())
    