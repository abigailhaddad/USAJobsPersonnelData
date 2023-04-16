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
df = pd.read_excel("../data/selected_cols.xlsx")

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, server_name="abigailhaddad1.pythonanywhere.com")

app.layout = html.Div([
    html.H1('Your Interactive DataFrame'),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        filter_action="native",  # Enables filtering
        sort_action="native",    # Enables sorting
        style_cell={'whiteSpace': 'normal', 'height': 'auto'},  # Fixes cell height and wrap text
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
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)
