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

# Define the layout
layout = dbc.Container(
    [
        html.H2('Delete Coach'),
        html.H4('Are you sure you want to remove this coach?'),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Proceed", id='deletecoach_go', n_clicks=0, color='danger', className='mr-2')
                ),
                dbc.Col(
                    dbc.Button("No", id='deletecoach_no', n_clicks=0, color='secondary')
                )
            ],
            className='mt-3'
        )
    ],
    className='mt-5',  # Adjust the top margin for centering
)

@app.callback(
    [
        Output('deletecoach_go', 'href')
    ],
    [
        Input('deletecoach_go', 'n_clicks'),
        Input('url', 'search')
    ]
)
def playerscore_delete(deletebtn, search):
    ctx = dash.callback_context
    # The ctx filter -- ensures that only a change in url will activate this callback
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'deletecoach_go' and deletebtn:
            sql = """ UPDATE coaches
                SET
                    coach_isdeleted = %s
                WHERE
                    coaches.coach_id = %s
            """

            parsed = urlparse(search)
            coachid = parse_qs(parsed.query)['id'][0]
            values = [True, coachid]

            db.modifydatabase(sql, values)

            return_href = '/coaches'

            return [return_href]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('deletecoach_no', 'href')
    ],
    [
        Input('deletecoach_no', 'n_clicks')
    ]
)
def playerscore_delete(deletebtn):
    ctx = dash.callback_context
    # The ctx filter -- ensures that only a change in url will activate this callback
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'deletecoach_no' and deletebtn:

            return_href = '/coaches'

            return [return_href]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate