# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 18:22:00 2023

@author: abiga
"""

import pickle
from typing import Any, List, Tuple

import numpy as np
import openai
import pandas as pd

# Load the API key from the file (change this to reflect where you've put
# your API key)
with open("../key/key.txt", "r") as key_file:
    api_key = key_file.read().strip()
    openai.api_key = api_key


def gen_list_of_occupations() -> List[str]:
    """
    Generates a list of occupation codes (OPM OCC codes) along with their corresponding
    occupational series names as comments.

    Returns:
    list: A list of formatted occupation codes with leading zeros if necessary.
    """

    list_of_raw_occupations = [
        "1529",  # Mathematician
        "1550",  # Computer Scientist
        "1515",  # Operations Research Analyst
        "0110",  # Economist
        "2210",  # Information Technology Management
        "1520",  # Mathematician Statistician
        "1530",  # Statistician
        "0800",  # Engineering
        "0100",  # Social Science, Psychology, and Welfare
        "1510",  # Actuary
        "0150",  # Geography
        "0343",  # Management and Program Analyst
        "0601",  # General Health Science
        "0400",  # Natural Resources Management and Biological Sciences
        "1300",  # General Physical Science
        "0130",  # Foreign Affairs
        "1517",  # Digital Forensics Examiner
        "1340",  # Meteorologist
        "1516",  # Cryptanalyst
        "1531",  # Statistician/Data Scientist
        "0401",  # General Natural Resources Management and Biological Sciences
        "1370",  # Cartographer
        "1372",  # Geodesist
        "1160",  # Financial Analysis
        "8960",  # Production Control
        "0500",  # Accounting and Budget
        "0340",  # Program Management
        "1306",  # Health Physicist
        "0685",  # Public Health Program Specialist
        "0187",  # Social Insurance Administrator
        "1330",  # Physical Scientist
        "1320",  # Chemist
        "1313",  # Geophysics
        "0560",  # Budget Analysis
        "0200",  # Human Resources Management
        "0391",  # Telecommunications
        "1035",  # Public Affairs
        "0690",  # Industrial Hygiene
        "0890",  # Agricultural Commodity Grading
        "1410",  # Librarian
        "1701",  # General Education and Training
        "0801",  # General Engineering
        "2010",  # Inventory Management
        "0809",  # Construction Control
        "1321",  # Metallurgist
        "1371",  # Cartographic Technician
        "0101",  # Social Science
        "0180",  # Psychology
        "0201",  # Human Resources Management
        "0341",  # Administrative Officer
        "0454",  # Soil Conservation
        "0696",  # Consumer Safety
        "0804",  # Fire Protection Engineering
        "0828",  # Equipment Services
        "0850",  # Electrical Engineering
        "0854",  # Computer Engineering
        "1301",  # General Physical Scientist
        "1308",  # Environmental Health
        "0501",  # Financial Administration and Program
        "0570",  # Financial Institutions Examining
        "0106",  # Insurance Accounts
        "0814",  # Mine Safety and Health
        "0193",  # Social Services
    ]
    list_of_occupations = [add_leading_zero(
        i) for i in list_of_raw_occupations]
    return list_of_occupations


def add_leading_zero(occupation_code: str) -> str:
    """
    Adds a leading zero to occupation codes with less than 4 digits.

    Args:
    occupation_code (str): The occupation code to format.

    Returns:
    str: The formatted occupation code with leading zeros if necessary.
    """
    return occupation_code.zfill(4)


def concatenate_columns(data_frame, columns, new_column_name='info'):
    """
    Concatenates the specified columns of a DataFrame into a new 'info' column.

    Args:
        data_frame (pd.DataFrame): The input DataFrame.
        columns (list): A list of column names to concatenate.
        new_column_name: A string with the name of the new column name

    Returns:
        pd.DataFrame: The DataFrame with the new 'new_column_name' column.
    """
    for column in columns:
        if column not in data_frame.columns:
            raise ValueError(f"Column '{column}' not found in the DataFrame.")

    # Convert each column to string and concatenate them into a new column
    data_frame[new_column_name] = data_frame[columns].astype(str).apply(' '.join, axis=1)

    return data_frame


def process_prompt(prompt, engine, temperature):
    """
    Processes a given prompt using the specified engine and temperature.

    Args:
        prompt (str): The input prompt.
        engine (str): The engine to be used for processing the prompt.
        temperature (float): The temperature to be used in processing the prompt.

    Returns:
        str: The response generated by the engine for the given prompt.
    """

    messages = [
        {"role": "user", "content": prompt}
    ]
    try:
        response = openai.ChatCompletion.create(
            model=engine,
            messages=messages,
            max_tokens=1024,
            temperature=temperature)
        return response.choices[0]['message']['content']
    except Exception as e:
        print(
            f"Error processing prompt. Engine: {engine}, Prompt: {prompt}, Error: {str(e)[:100]}")
        return ''


def gpt_calls(sample: pd.DataFrame) -> pd.DataFrame:
    """
    Processes a sample DataFrame by calling the GPT engine for each row, generating a filtered DataFrame with additional columns for occupation, job duties, and job qualifications.

    Args:
        sample (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The filtered DataFrame with additional columns for occupation, job duties, and job qualifications.
    """

    engine = 'gpt-3.5-turbo'
    temperature = 0.1

    # Create empty lists to store results for both prompts
    results_prompt_1 = []

    # Iterate through the dataframe and process each prompt
    for _, row in sample.iterrows():

        # Process first prompt
        prompt_1 = f"I'm going to give you text from a federal job listing that I'd like you to categorize as whether it would be a good job for someone who is interested in data science tasks like writing code to clean and analyze data, do modelling, automate processes related to data, using tools like R, SQL, and Python. But I need you to keep in mind that these listings are different from private sector listings in that they frequently use different vocabulary to talk about those tasks, and they don’t list specific tools or languages, so I need you to think broadly and make a guess. I’d like you to include leadership jobs involving data, if you think they still involve some analysis and coding, and also to include jobs which have data science components and also require significant background in a specific topic like economics or physical science. I also do want to include data engineering jobs, but exclude pure software engineering jobs and software development and IT jobs. Please structure your response starting with Yes or No and then explaining your reasoning.: {row['info']}"

        response_1 = process_prompt(prompt_1, engine, temperature)
        results_prompt_1.append(response_1)

    sample['occupation'] = results_prompt_1

    # Filter the dataframe to only include rows where the response starts with "Yes"
    sample_filtered = sample[sample['occupation'].str.startswith('Yes')]

    # Define additional prompts
    additional_prompts_dict = {
        "job_duties": "In TWO sentences, using accessible, jargon-free languge, summarize JUST the specific things about the job description -- leave out anything generic, anything related to the application process, or the agency-- JUST what the job does.",
        "job_qualifications": "in TWO sentences, using jargon-free language, summarize educational and career background requirements for being hired, excluding generic things like attention to detail."}

    # Iterate through the additional prompts and process them
    for prompt_key in additional_prompts_dict.keys():
        prompt_text = additional_prompts_dict[prompt_key]
        prompt_results = []

        for _, row in sample_filtered.iterrows():
            prompt = f"Here is the job listing again: {row['info']} {prompt_text}"
            response = process_prompt(prompt, engine, temperature)
            prompt_results.append(response)

        # Add the results as a new column in the filtered dataframe
        sample_filtered[prompt_key] = prompt_results

    # Combine the "Yes" and "No" occupation results into a single DataFrame
    sample_nos = sample[~sample['occupation'].str.startswith('Yes')]
    yes_and_no = sample_nos.append(sample_filtered)

    return yes_and_no



def sample_data(data, n=30):
    """
    Returns a random sample of n rows from the input DataFrame.

    Args:
        data (pd.DataFrame): The input DataFrame.
        n (int): The number of rows to sample.

    Returns:
        pd.DataFrame: The randomly sampled DataFrame with n rows.
    """

    random_sample = data.sample(n, random_state=1)
    return (random_sample)


def read_data_from_file(file_path: str) -> Any:
    """
    Reads data from the specified file path.

    Args:
        file_path (str): The path of the file to read the data from.

    Returns:
        Any: The data read from the file.
    """
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    return data


def find_metrics(data_frame: pd.DataFrame) -> None:
    """
    Finds and prints several metrics from the given DataFrame.

    Args:
        data_frame (pd.DataFrame): The input DataFrame to analyze.
    """
    data_frame['Yes_or_No'] = np.where(data_frame['occupation'].str[0:3] == "Yes", "Yes", "No")

    # What percent got classified as data science?
    print(data_frame['Yes_or_No'].value_counts(normalize=True))

    # How many of them have 'data sci' in them?
    data_frame['has_data_sci'] = np.where(
        data_frame['info'].str.lower().str.contains("data sci"),
        "data sci",
        "not")
    print(pd.crosstab(data_frame['Yes_or_No'], data_frame['has_data_sci']))

    # Examples of yesses without 'data sci'
    yes_no_data_sci = data_frame.loc[(data_frame['has_data_sci'] == "not")
                             & (data_frame['Yes_or_No'] == "Yes")]

    # Random 5
    yes_no_data_sci.sample(5)[["PositionTitle", "occupation"]].to_excel(
        "5 selected data sci jobs without data sci.xlsx")
    pure_data_sci = yes_no_data_sci = data_frame.loc[(data_frame['has_data_sci'] != "not")]
    print(len(pure_data_sci))


def extract_min_max(salary_list: List[dict]) -> Tuple[float, float]:
    """
    Extracts the minimum and maximum salary values from the given salary list.

    Args:
        salary_list (List[dict]): A list of dictionaries containing salary information.

    Returns:
        Tuple[float, float]: The minimum and maximum salary values, or None for both if the list is empty.
    """
    if len(salary_list) > 0:
        min_salary = float(salary_list[0]['MinimumRange'])
        max_salary = float(salary_list[0]['MaximumRange'])
    else:
        min_salary, max_salary = None, None
    return min_salary, max_salary


def extract_location_names(location_list: List[dict]) -> str:
    """
    Extracts the location names from the given location list.

    Args:
        location_list (List[dict]): A list of dictionaries containing location information.

    Returns:
        str: A string containing the extracted location names, separated by semicolons.
    """
    location_names = [location['LocationName'] for location in location_list]
    return '; '.join(location_names)


def clean_for_app(data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the given DataFrame to keep only the necessary columns and formats the data for the application.

    Args:
        data_frame (pd.DataFrame): The input DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame with only the necessary columns.
    """
    data_frame['Close Date'] = pd.to_datetime(
        data_frame['ApplicationCloseDate'],
        errors='coerce').dt.strftime('%m-%d-%Y')
    data_frame['Min_salary'], data_frame['Max_salary'] = zip(
        *data_frame['PositionRemuneration'].apply(extract_min_max))
    data_frame['Location'] = data_frame['PositionLocation'].apply(extract_location_names)
    keep_cols = [
        'PositionTitle',
        'DepartmentName',
        'OrganizationName',
        'occupation',
        'job_duties',
        'job_qualifications',
        'PositionURI',
        'HiringPath',
        'Close Date',
        'Min_salary',
        'Max_salary',
        'Location']
    return data_frame[keep_cols]

def filter_func(x, list_of_occupations):
    """
    Filters a list of dictionaries `x` to include only those dictionaries whose 'Code' value 
    matches one of the codes in the list `listofoccupations`.

    Parameters:
    -----------
    x : list
        A list of dictionaries, each of which contains a 'Code' key.
    list_of_occupations : list
        A list of occupation codes to filter on.

    Returns:
    --------
    bool
        Returns True if any of the 'Code' values in `x` match any of the codes in `listofoccupations`, 
        False otherwise.
    """
    return any(code in [entry['Code'] for entry in x] for code in list_of_occupations)

def main():
    current_data = read_data_from_file("../data/currentResults.pkl")
    # Define the columns to be concatenated
    columns = [
        "QualificationSummary",
        "JobSummary",
        "MajorDuties",
        "Education",
        "Evaluations"]
    # Concatenate the specified columns into a new 'info' column in the
    # DataFrame
    current_data = concatenate_columns(current_data, columns)
    # Generate the list of occupations (OPM OCC codes)
    list_of_occupations = gen_list_of_occupations()
    # Define a custom lambda function to check if a code from the list exists
    # in the value
    # Apply the custom function and filter the DataFrame based on the
    # occupation codes
    filtered_data_occ = current_data[current_data['JobCategory'].apply(filter_func, list_of_occupations=list_of_occupations)]
    # Filter the DataFrame to include only rows where the 'info' column
    # contains the word "data"
    jobs_with_data = filtered_data_occ.loc[filtered_data_occ['info'].str.lower(
    ).str.count("data") >= 2]
    # Get a random sample of 1000 rows from the filtered DataFrame
    sample = sample_data(jobs_with_data, 1000)
    # Process the  DataFrame using the GPT engine and return the final
    # DataFrame with additional columns
    data_frame = gpt_calls(sample)
    # Define the columns to be kept and written out
    # find_metrics(data_frame)
    cleaned_for_app = clean_for_app(data_frame)
    return(cleaned_for_app)
    
if __name__ == "__main__":
    cleaned_for_app=main()
    cleaned_for_app.to_pickle("../data/file_for_app_sample.pkl")
