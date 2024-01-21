import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from urllib.parse import urlparse, parse_qs
import pandas as pd
from dash.dash_table.Format import Group
import plotly.express as px

from app import app
from apps import dbconnect as db


layout = dbc.Container(
    [
        html.H2('Delete Player Score'),
        html.H4('Are you sure you want to delete this player score?'),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Proceed", id='playerscore_delete', n_clicks=0, color='danger', className='mr-2')
                ),
                dbc.Col(
                    dbc.Button("No", id='playerscore_nodelete', n_clicks=0, color='secondary')
                )
            ],
            className='mt-3'
        )
    ],
    className='mt-5',  
)

@app.callback(
    [
        Output('playerscore_delete', 'href')
    ],
    [
        Input('playerscore_delete', 'n_clicks'),
        Input('url', 'search')
    ]
)
def playerscore_delete(deletebtn, search):
    ctx = dash.callback_context
   
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'playerscore_delete' and deletebtn:
            sql = """ UPDATE playerscore
                SET
                    playerscore_isdeleted = %s
                WHERE
                    playerscore.score_id = %s
            """

            parsed = urlparse(search)
            scoreid = parse_qs(parsed.query)['id'][0]
            values = [True, scoreid]

            db.modifydatabase(sql, values)

            href_sql = """ SELECT skill_id
                FROM
                    playerscore
                WHERE
                    playerscore.score_id = %s
            """

            href_values = [scoreid]
            href_columns = ['Skill ID']

            df = db.querydatafromdatabase(href_sql, href_values, href_columns)
            skillid = df.iloc[0]['Skill ID']

            return_href = f'/skillstest/skillstestdetails?mode=edit&id={skillid}'

            return [return_href]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('playerscore_nodelete', 'href')
    ],
    [
        Input('playerscore_nodelete', 'n_clicks'),
        Input('url', 'search')
    ]
)
def playerscore_delete(deletebtn, search):
    ctx = dash.callback_context
    
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'playerscore_nodelete' and deletebtn:
            parsed = urlparse(search)
            scoreid = parse_qs(parsed.query)['id'][0]

            href_sql = """ SELECT skill_id
                FROM
                    playerscore
                WHERE
                    playerscore.score_id = %s
            """

            href_values = [scoreid]
            href_columns = ['Skill ID']

            df = db.querydatafromdatabase(href_sql, href_values, href_columns)
            skillid = df.iloc[0]['Skill ID']

            return_href = f'/skillstest/skillstestdetails?mode=edit&id={skillid}'

            return [return_href]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate