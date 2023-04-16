# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 22:40:57 2023

@author: abiga
"""

import dash
import dash_table
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

# Load your DataFrame
df = pd.read_csv("/home/abigailhaddad1/projects/USAJobs/data/selected_cols_cleaned.csv")
df["Close Date"]=pd.to_datetime(df['Close Date'])

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, url_base_pathname='/usajobs/')
server = app.server  # Add this line

def generate_tooltip_data(df):
    tooltip_data = []

    for i in range(len(df)):
        tooltip_row = {}
        for col in df.columns:
            tooltip_row[col] = {'value': df.at[i, col], 'type': 'markdown'}
        tooltip_data.append(tooltip_row)

    return tooltip_data

tooltip_data = generate_tooltip_data(df)


app.layout = html.Div([
    html.H1('Selection of USAJobs Listings With Data Science Tasks'),
    html.Div([
        html.Label('Filter by Salary Range:'),
        dcc.RangeSlider(
            id='salary-range-slider',
            min=0,
            max=200000,
            step=1000,
            value=[30000, 100000],
            marks={i: f'${i:,}' for i in range(0, 200001, 20000)},
        ),
        html.Div(id='slider-output-container')
    ]),
    html.Div([
        html.Label('Filter by Close Date Range:'),
        dcc.RangeSlider(
            id='date-range-slider',
            min=int(df['Close Date'].min().timestamp()),
            max=int(df['Close Date'].max().timestamp()),
            step=86400,  # One day step size
            value=[
                int(df['Close Date'].min().timestamp()),
                int(df['Close Date'].max().timestamp())
            ],
            marks={
                int(ts.timestamp()): ts.strftime('%Y-%m-%d')
                for ts in pd.date_range(df['Close Date'].min(), df['Close Date'].max(), freq='1M')
            },
        ),
        html.Div(id='date-slider-output-container')
    ]),
    dash_table.DataTable(
        column_selectable='multi',
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
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
