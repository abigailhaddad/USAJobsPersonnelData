# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 22:40:57 2023

@author: abiga
"""

import pickle
from typing import Any

import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd


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


def clean_df(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the DataFrame with required modifications.

    Args:
        dataframe (pd.DataFrame): The input DataFrame to clean.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    dataframe["Close Date"] = pd.to_datetime(dataframe['Close Date']).dt.strftime('%Y-%m-%d')
    dataframe["Min_salary"] = dataframe["Min_salary"].astype(int)
    dataframe["Max_salary"] = dataframe["Max_salary"].astype(int)
    dataframe['HiringPath'] =  dataframe['HiringPath'].astype(str)
    return dataframe


raw_df = read_data_from_file("../data/file_for_app_sample.pkl")
cleaned_df = clean_df(raw_df)

min_timestamp = int(pd.to_datetime(cleaned_df['Close Date']).min().timestamp())
max_timestamp = int(pd.to_datetime(cleaned_df['Close Date']).max().timestamp())

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, url_base_pathname='/usajobs/')
server = app.server


def generate_tooltip_data(cleaned_df: pd.DataFrame) -> list:
    """
    Generates the tooltip data for the dash_table.DataTable.

    Args:
        cleaned_df (pd.DataFrame): The cleaned DataFrame.

    Returns:
        list: The list of tooltip data dictionaries.
    """
    tooltip_data = []

    for i in range(len(cleaned_df)):
        tooltip_row = {}
        for col in cleaned_df.columns:
            tooltip_row[col] = {'value': str(cleaned_df.iloc[i][col]), 'type': 'markdown'}
        tooltip_data.append(tooltip_row)

    return tooltip_data



tooltip_data = generate_tooltip_data(cleaned_df)
lowest_min_salary = int(cleaned_df['Min_salary'].min() // 10000) * 10000
highest_max_salary = int((cleaned_df['Max_salary'].max() + 9999) // 10000) * 10000


@app.callback(
    Output('table', 'data'),
    Input('salary-range-slider', 'value'),
    Input('date-range-slider', 'value')
)
def filter_data(salary_range, date_range):
    """
    Filters the data based on salary and date ranges.

    Args:
        salary_range (list): A list containing the minimum and maximum salary.
        date_range (list): A list containing the minimum and maximum dates as timestamps.

    Returns:
        list: The filtered data as a list of dictionaries.
    """
    dff = cleaned_df.copy()

    # Create a new 'Close Date Datetime' column with datetime objects
    dff["Close Date Datetime"] = pd.to_datetime(dff["Close Date"])

    # Filter by salary range
    min_salary, max_salary = salary_range
    dff = dff[((dff['Min_salary'] <= max_salary) &
               (dff['Max_salary'] >= min_salary))]

    # Filter by date range
    min_date, max_date = pd.to_datetime(date_range, unit='s')
    dff = dff[(dff['Close Date Datetime'] >= min_date) & (dff['Close Date Datetime'] <= max_date)]

    # Remove the 'Close Date Datetime' column
    dff = dff.drop(columns=['Close Date Datetime'])
    
    

    return dff.to_dict('records')



app.layout = html.Div([
    html.H1('Selection of USAJobs Listings With Data Science Tasks'),
    html.Div([
        html.Label('Filter by Salary Range:'),
        dcc.RangeSlider(
            id='salary-range-slider',
            min=lowest_min_salary,
            max=highest_max_salary,
            step=1000,
            value=[lowest_min_salary, highest_max_salary],
            marks={i: f'${i:,}' for i in range(lowest_min_salary, highest_max_salary + 1, 20000)},
        ),
        html.Div(id='slider-output-container')
    ]),
    html.Div([
        html.Label('Filter by Close Date Range:'),
        dcc.RangeSlider(
            id='date-range-slider',
            min=min_timestamp,
            max=max_timestamp,
            step=86400,  # One day step size
            value=[
                min_timestamp,
                max_timestamp],
            marks={
                int(ts.timestamp()): ts.strftime('%Y-%m-%d')
                for ts in pd.date_range(cleaned_df['Close Date'].min(), cleaned_df['Close Date'].max(), freq='1M')
            },
        ),
        html.Div(id='date-slider-output-container')
    ]),
    dash_table.DataTable(
        column_selectable='multi',
        id='table',
        columns=[{"name": i, "id": i} for i in cleaned_df.columns],
        data=cleaned_df.to_dict('records'),
        filter_action="native",  # Enables filtering
        sort_action="native",    # Enables sorting
        style_cell={
            'whiteSpace': 'nowrap',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
        style_data={
            'maxWidth': '150px',  # Adjust this value to control the column width
        },
        style_data_conditional=[  # Adjusts font size
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_header={  # Header style
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        export_format='csv',  # Enables CSV export
        export_headers='display',  # Uses displayed header names in the exported file
        tooltip_data=tooltip_data,
        tooltip_duration=None,  # Set this property to keep the tooltip open indefinitely
    ),
])


if __name__ == '__main__':
    app.run_server(debug=True)
