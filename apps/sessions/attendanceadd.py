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
        Output('attendanceadd_session','children')
    ],
    [
        Input('url','pathname')
    ],
    [
        State('url','search')
    ]
)
def attendance_view(pathname, search):
    if pathname == '/sessions/attendanceadd':
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
                        id='attendanceadd_back',
                        color = 'secondary',
                    ),
                    width=4,
                    className='mb-3'
                ),
                html.H2('Add Attendance'),
            ],style={'width': '1000px', 'margin': 'auto'}, className='mb-3'
        ),
        html.Hr(style={'width': '1000px', 'margin': 'auto'}, className='mb-3'),
        dbc.Alert(id='attendanceadd_alert', is_open=False, style={'width': '1000px', 'margin': 'auto'}, className='mb-3'),
        dbc.Row(
            html.Div(
                "session details go here",
                id='attendanceadd_session',
                style={'width': '1000px', 'margin': 'auto'}, className='mb-3'
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader('Add Players Attended', style={'font-weight': '600'}),
                            dbc.CardBody(
                                [
                                    html.Div(
                                        [
                                            dbc.Form(
                                                [
                                                    dbc.Row(
                                                        [
                                                            html.Div(
                                                                [
                                                                    html.Label('Select Players'),
                                                                    dcc.Dropdown(id='attendanceadd_players_dropdown',
                                                                                 placeholder='Choose Player Names',
                                                                                 multi=True)
                                                                ]
                                                            )
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    dbc.Col(
                                            dbc.Button(
                                                'Submit',
                                                id='attendanceadd_submit',
                                                n_clicks=0
                                            ),
                                            width=3,
                                            style={'marginTop':20}
                                    )
                                ]
                            ),
                            
                        ],
                        style={'width': '1000px', 'margin': 'auto'}  
                    )
                )
            ]
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(
                    html.H4('Save Success')
                ),
                dbc.ModalBody(
                    ['Message here! Edit me please!'], id='attendanceadd_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/sessions',
                        id='attendanceadd_btn_modal'
                    )
                )
            ],
            centered=True,
            id='attendanceadd_successmodal',
            backdrop='static'
        )
    ]
)

@app.callback(
    Output('attendanceadd_players_dropdown', 'options'),
    [Input('url', 'pathname')],
     [State('url','search')]
)
def attendanceadd_populate_players_dropdown(pathname, search):
    if pathname == '/sessions/attendanceadd':
        player_sql = """SELECT CONCAT(P.player_lastname, ', ', P.player_firstname, ' ', P.player_middlename) AS label, P.player_id AS value
            FROM Players P
            JOIN Coaches C ON P.group_id = C.group_id AND P.program_id = C.program_id
            JOIN CoachAssignment CA ON C.coach_id = CA.coach_id
            WHERE CA.session_id = %s;
            """

        parsed = urlparse(search)
        sessionid = parse_qs(parsed.query)['id'][0]
        values = [sessionid]
        cols=['label','value']

        df = db.querydatafromdatabase(player_sql, values, cols)

        player_options = df.to_dict('records')
        return player_options
    else:
        raise PreventUpdate
    
@app.callback(
    [
        Output('attendanceadd_alert','color'),
        Output('attendanceadd_alert','children'),
        Output('attendanceadd_alert','is_open'),
        Output('attendanceadd_successmodal','is_open'),
        Output('attendanceadd_feedback_message','children'),
        Output('attendanceadd_btn_modal','href')
    ],
    [
        Input('attendanceadd_submit','n_clicks')
    ],
    [
        State('attendanceadd_players_dropdown','value'),
        State('url','search')
    ]
)
def save_attendance(submit_btn, selected_players, search):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'attendanceadd_submit' and submit_btn:
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            feedbackmessage=''
            okay_href=''

            if not selected_players:
                alert_open=True
                alert_color='danger'
                alert_text='Check your inputs. Please choose players'
            else:
                parsed = urlparse(search)
                session_id=parse_qs(parsed.query)['id'][0]

                all_players_valid = True  
                for player_id in selected_players:
                    sql = """SELECT T.transaction_id, T.status_id
                             FROM transactions T
                             WHERE T.player_id = %s AND T.transaction_id IS NOT NULL
                             ORDER BY T.payment_date DESC
                             LIMIT 1
                    """
                    values = [player_id]
                    result = db.querydatafromdatabase(sql, values, ['transaction_id', 'status_id'])

                    if not result.empty:
                        transaction_id = int(result.iloc[0]['transaction_id'])
                        status_id = int(result.iloc[0]['status_id'])

                        if status_id == 2:  
                            player_name_sql = """SELECT CONCAT(player_lastname, ', ', player_firstname, ' ', player_middlename) AS player_name
                                                 FROM Players
                                                 WHERE player_id = %s
                            """
                            player_name = db.querydatafromdatabase(player_name_sql, [player_id], ['player_name']).iloc[0]['player_name']

                            alert_open = True
                            alert_color = 'danger'
                            alert_text = f'Player {player_name} is marked as Inactive. Please contact parent.'
                            all_players_valid = False  
                        else:
                            sql_insert = """INSERT INTO PlayerAttendance (transaction_id, session_id)
                                            VALUES (%s, %s)
                            """
                            values_insert = [transaction_id, session_id]
                            db.modifydatabase(sql_insert, values_insert)

                            feedbackmessage = 'Attendance has been saved.'
                    else:
                       
                        player_name_sql = """SELECT CONCAT(player_lastname, ', ', player_firstname, ' ', player_middlename) AS player_name
                                             FROM Players
                                             WHERE player_id = %s
                        """
                        player_name = db.querydatafromdatabase(player_name_sql, [player_id], ['player_name']).iloc[0]['player_name']

                        alert_open = True
                        alert_color = 'danger'
                        alert_text = f'No valid transaction for player {player_name}.'
                        all_players_valid = False  

                if all_players_valid:
                    modal_open = True  
                    okay_href = '/sessions'
        return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]
    else:
        raise PreventUpdate
        

            
