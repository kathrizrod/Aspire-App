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
        html.H2('Skills Test'),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                dbc.Button(
                                    "Add Skills Test", color="secondary",
                                    href='/skillstest/skillstestprofile'
                                )
                            ]
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                html.H4('Find Skills Test'),
                                html.Div(
                                    dbc.Form(
                                        dbc.Row(
                                            [
                                                dbc.Label("Search", width=1),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id="skillstest_titlefilter",
                                                        placeholder='Skills Test Name'
                                                    ),
                                                    width=5
                                                )
                                            ],
                                            className='mb-3'
                                        )
                                    )
                                ),
                                html.Div(
                                    [
                                        dbc.Col(
                                            "Table of skills test goes here",
                                            id='skillstest_list',
                                            style={'text-align': 'center'}  
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
        Output('skillstest_list', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('skillstest_titlefilter', 'value'),
    ]
)
def home_skillstestlist(pathname, searchterm):
    if pathname == '/skillstest':
        
        sql = """ SELECT skill_name, skill_desc, skill_ins, skill_scoreunit, skill_id
            FROM skillstest
            WHERE skill_isdeleted = FALSE
        """

        values = []
        cols = ['Skills Test', 'Description', 'Instructions', 'Metric', 'ID']

        if searchterm:
            sql += " AND skill_name ILIKE %s"
            values += [f"%{searchterm}%"]

        df = db.querydatafromdatabase(sql, values, cols)
    
        if df.shape:
            buttons = []
            for skill_id in df['ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Open', href=f'/skillstest/skillstestdetails?mode=edit&id={skill_id}', size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                ]
            df['Scores'] = buttons
            df = df[['Skills Test', 'Description', 'Instructions', 'Metric', 'Scores']]

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]

        else:
            return["No records to display"]
    else:
        raise PreventUpdate

