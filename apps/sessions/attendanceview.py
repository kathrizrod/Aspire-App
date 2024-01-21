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

@app.callback(
    [
        Output('attendance_list','children')
    ],
    [
        Input('url','pathname')
    ],
    [
        State('url','search')
    ]
)
def attendance_view(pathname, search):
    if pathname == '/sessions/attendanceview':
        sql="""SELECT DISTINCT CONCAT(P.player_firstname, ' ', P.player_lastname) AS player_name
            FROM Players P
            JOIN transactions T ON P.player_id = T.player_id
            JOIN PlayerAttendance PA ON T.transaction_id = PA.transaction_id
            JOIN TrainingSession TS ON PA.session_id = TS.session_id
            WHERE TS.session_id = %s
            """
        parsed=urlparse(search)
        sessionid = parse_qs(parsed.query)['id'][0]
        values=[sessionid]
        cols=['Name']

        df = db.querydatafromdatabase(sql, values, cols)
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
        return[table]
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('attendance_session','children')
    ],
    [
        Input('url','pathname')
    ],
    [
        State('url','search')
    ]
)
def attendance_view(pathname, search):
    if pathname == '/sessions/attendanceview':
        sql="""SELECT DISTINCT P.program_name, AG.group_name, TS.session_date, S.schedule_dotw, S.schedule_time, CONCAT(C.coach_firstname, ' ', C.coach_lastname) AS coach_name
        FROM TrainingSession TS
        JOIN Schedules S ON TS.schedule_id = S.schedule_id
        JOIN Coaches C ON C.coach_id = (
            SELECT coach_id
            FROM CoachAssignment CA
            WHERE CA.session_id = TS.session_id
            )
        JOIN FBPrograms P on c.program_id = p.program_id
        JOIN AgeGroups AG ON C.group_id = AG.group_id
        WHERE TS.session_id = %s
        ORDER BY TS.session_date DESC"""

        parsed=urlparse(search)
        sessionid = parse_qs(parsed.query)['id'][0]
        values=[sessionid]
        cols=['Program','Age Group','Date','Day','Time','Coach']

        df = db.querydatafromdatabase(sql, values, cols)
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
        return[table]
    else:
        raise PreventUpdate


layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        "Back",
                        href = '/sessions',
                        id='attendanceview_back',
                        color = 'secondary',
                    ),
                    width=4,
                    className='mb-3'
                ),
                html.H2('Attendance'),
            ],style={'width': '1000px', 'margin': 'auto'}, className='mb-3'
        ),
        html.Hr(style={'width': '1000px', 'margin': 'auto'}, className='mb-3'),
        dbc.Row(
            html.Div(
                "session details go here",
                id='attendance_session',
                style={'width': '1000px', 'margin': 'auto'}, className='mb-3'
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader('Players Attended', style={'font-weight': '600'}),
                            dbc.CardBody(
                                [
                                    html.Div(
                                        [
                                            dbc.Form(
                                                [
                                                    dbc.Row(
                                                        html.Div(
                                                            "Table goes here",
                                                            id='attendance_list'
                                                        )
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            ),
                        ],
                        style={'width': '1000px', 'margin': 'auto'} 
                    )
                )
            ]
        ),
    ]
)