import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2('Coaches'),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                dbc.Button(
                                    "Add Coach", color="secondary",
                                    href='/coaches/addcoach'
                                )
                            ]
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Label("Search", width=1),
                                        dbc.Col(
                                            dbc.Input(id='coach_titlefilter', type='text', placeholder='By Coach Name'),
                                            width=5
                                        )
                                    ],
                                    className='mb-3'
                                ),
                                dbc.Row(
                                    [
                                        dbc.Label("Sort By:", width=1),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id='sorting_dropdown',
                                                options=[
                                                    {'label': 'Coach Name', 'value': 'Coach Name'},
                                                    {'label': 'Age Group', 'value': 'Age Group'},
                                                    {'label': 'Program', 'value': 'Program'}
                                                ],
                                                value='Coach Name',  # Default sorting criterion
                                                clearable=False,
                                                style={'width': '100%'}
                                            ),
                                            width=3
                                        )
                                    ],
                                    className='mb-3'
                                ),
                                html.Div(
                                    [
                                        dbc.Col(
                                            "Table of coaches goes here",
                                            id='coach_list',
                                            style={'text-align': 'center'}  # Center the content of the table
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    [
        Output('coach_list', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('coach_titlefilter', 'value'),
        Input('sorting_dropdown', 'value')
    ]
)
def coachlist(pathname, searchterm, sortby):
    if pathname == '/coaches':
        sql = """
            SELECT
                coaches.coach_firstname || ' ' || coaches.coach_lastname AS coach_name,
                agegroups.group_name,
                fbprograms.program_name,
                coaches.coach_id
            FROM
                coaches 
            JOIN agegroups ON coaches.group_id = agegroups.group_id
            JOIN fbprograms ON coaches.program_id = fbprograms.program_id
            WHERE coach_isdeleted = FALSE
        """

        values = []
        cols = ['Coach Name', 'Age Group', 'Program', 'ID']

        if searchterm:
            sql += " AND coaches.coach_firstname || ' ' || coaches.coach_lastname ILIKE %s"
            values += [f"%{searchterm}%"]
        
        if sortby == 'Coach Name':
            sql += "\nORDER BY coaches.coach_firstname || ' ' || coaches.coach_lastname ASC"
        elif sortby == 'Age Group':
            sql += "\nORDER BY agegroups.group_name ASC"
        elif sortby == 'Program':
            sql += "\nORDER BY fbprograms.program_name ASC"

        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            buttons = []
            for coach_id in df['ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Delete', href=f'/coaches/deletecoach?mode=edit&id={coach_id}', size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                ]
            df['Delete?'] = buttons
            df = df[['Coach Name', 'Age Group', 'Program', 'Delete?']]

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]

        else:
            return["No records to display"]
    else:
        raise PreventUpdate