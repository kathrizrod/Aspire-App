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
        Output('sessions_upcominglist','children')
    ],
    [
        Input('url','pathname')
    ]
)
def sessions_loadupcominglist(pathname):
    if pathname=='/sessions':
        sql="""SELECT DISTINCT P.program_name, AG.group_name, TS.session_date, S.schedule_dotw, S.schedule_time, CONCAT(C.coach_firstname, ' ', C.coach_lastname) AS coach_name
        FROM trainingsession TS
        JOIN schedules S ON TS.schedule_id = S.schedule_id
        JOIN coaches C ON C.coach_id = (
            SELECT coach_id
            FROM coachassignment CA
            WHERE CA.session_id = TS.session_id
            )
        JOIN fbprograms P on c.program_id = p.program_id
        JOIN agegroups AG ON C.group_id = AG.group_id
        WHERE TS.session_date > CURRENT_DATE
        ORDER BY TS.session_date DESC"""

        values=[]
        cols=['Program','Age Group','Date','Day','Time','Coach']

        df=db.querydatafromdatabase(sql, values, cols)

        table = html.Div(
                dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm'),
                style={'height':'400px','overflowY':'scroll'})
        
        return [table]
    else:
        raise PreventUpdate
    
@app.callback(
    [
        Output('sessions_previouslist','children')
    ],
    [
        Input('url','pathname')
    ]
)
def sessions_loadpreviouslist(pathname):
    if pathname =='/sessions':
        sql="""SELECT P.program_name, AG.group_name, TS.session_date, S.schedule_dotw, S.schedule_time, CONCAT(C.coach_firstname, ' ', C.coach_lastname) AS coach_name, TS.session_id,
        CASE WHEN PA.attendance_id IS NOT NULL THEN 'Yes' ELSE 'No' END AS has_attendance
        FROM trainingsession TS
        JOIN schedules S ON TS.schedule_id = S.schedule_id
        JOIN programschedule PS ON TS.schedule_id = PS.schedule_id
        JOIN fbprograms P ON PS.program_id = P.program_id
        JOIN coaches C ON C.coach_id = (
            SELECT coach_id
            FROM coachassignment CA
            WHERE CA.session_id = TS.session_id
            )
        JOIN agegroups AG ON C.group_id = AG.group_id
        LEFT JOIN playerattendance PA ON TS.session_id = PA.session_id
        WHERE TS.session_date < CURRENT_DATE
        ORDER BY TS.session_date DESC"""

        values=[]
        cols=['Program','Age Group','Date','Day','Time','Coach','ID', 'Has Attendance']

        df=db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            buttons=[]
            for index, row in df.iterrows():
                button_label = 'Add' if row['Has Attendance']=='No' else 'View'
                button_color = 'secondary' if button_label == 'View' else 'warning'
                button_href = f'sessions/attendanceadd?mode=add&id={row["ID"]}' if button_label == 'Add' else f'sessions/attendanceview?mode=view&id={row["ID"]}'
                buttons += [
                    html.Div(
                        dbc.Button(button_label,href=button_href,
                                   size='sm',color=button_color),
                                   style={'text-align':'center'}
                    )
                ]
            df['Attendance']=buttons
            df = df[['Program','Age Group','Date','Day','Time','Coach','Attendance']]

            table = html.Div(
                dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm'),
                style={'height':'400px','overflowY':'scroll'})
        
            return [table]
        else:
            return['No records to display']
    else:
        raise PreventUpdate

layout = html.Div(
        [
        html.H2('Training Sessions'),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                    [
                        dbc.CardHeader('Upcoming Sessions',style={'font-weight': '600'}),
                        dbc.CardBody(
                            [
                                html.Div(
                                    [
                                        dbc.Button(
                                            "Add Session", color='secondary',
                                            href='/sessions/sessionsadd?mode=add',
                                        )
                                    ],
                                    className='d-flex justify-content-end'
                                ),
                                html.Hr(),
                                html.Div(
                                    "Table of Sessions goes here",
                                    id='sessions_upcominglist',
                                )
                            ]
                        )
                    ]
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader('Previous Sessions',style={'font-weight': '600'}),
                            dbc.CardBody(
                                [
                                    html.Div(
                                            "Table of previous sessions goes here",
                                            id='sessions_previouslist'
                                    )
                                ]
                            )
                        ]
                    )
                )
            ]
        )
    ]
)

