import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from urllib.parse import urlparse, parse_qs
import pandas as pd

from app import app
from apps import dbconnect as db

from datetime import datetime

@app.callback(
    [Output('session_dotw', 'children')],
    [Input('session_date', 'date')]
)
def sessionsadd_showdotw(date):
    if date:
        
        selected_date = datetime.strptime(date, '%Y-%m-%d')
        
       
        day_of_week = selected_date.strftime('%A')

        return [f'{day_of_week}']
    else:
        return ['']
    
@app.callback(
        [Output('session_agegroup','children')],
        [Input('session_coach','value')]
)
def sessionadd_showagegroup(coach):
    if coach:
        sql="""SELECT a.group_name
        FROM agegroups a
        JOIN coaches c ON a.group_id=c.group_id
        WHERE c.coach_id=%s"""
        values=[coach]
        cols=['Age Group']

        df = db.querydatafromdatabase(sql, values, cols)

        agegroup=df['Age Group'].iloc[0]

        sessionagegroup = html.Div(agegroup)

        return [sessionagegroup]
    else:
        raise None
    
@app.callback(
        [Output('session_fbprogram','children')],
        [Input('session_coach','value')]
)
def sessionadd_showafbprogram(coach):
    if coach:
        sql="""SELECT p.program_name
        FROM fbprograms p
        JOIN coaches c ON c.program_id=p.program_id
        WHERE c.coach_id=%s"""
        values=[coach]
        cols=['Football Program']

        df = db.querydatafromdatabase(sql, values, cols)

        fbprogram=df['Football Program'].iloc[0]

        sessionsfbprogram = html.Div(fbprogram)

        return [sessionsfbprogram]
    else:
        raise None
    
@app.callback(
    Output('session_newschedule','children'),
    [Input('session_schedule','value')]
)
def sessionsadd_addnewschedule(newschedule):
    if newschedule != 'new_schedule':
        newinput=dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Label("Time",width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='newschedule_time',
                                placeholder="00:00 AM/PM - 00:00 AM/PM",
                                disabled=True
                            ),
                            width=4
                        )
                    ],
                    className='mb-3'
                )
            ]
        )
    else:
        newinput=dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Label("Time",width=2),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='newschedule_time',
                                placeholder="00:00 AM/PM - 00:00 AM/PM",
                            ),
                            width=4
                        )
                    ],
                    className='mb-3'
                )
            ]
        )
    return newinput

layout = html.Div(
    [
        html.H2('Add New Session',style={'width': '1000px', 'margin': 'auto'}, className='mb-3'),
        html.Hr(style={'width': '1000px', 'margin': 'auto'}, className='mb-3'),
        dbc.Alert(id='sessionsadd_alert', is_open=False, style={'width': '1000px', 'margin': 'auto'}, className='mb-3'),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader('Session Details', style={'font-weight': '600'}),
                            dbc.CardBody(
                                [
                                    html.Div(
                                        [
                                            dbc.Form(
                                                [
                                                    dbc.Row(
                                                        [
                                                            dbc.Label("Coach", width=2),
                                                            dbc.Col(
                                                                dcc.Dropdown(
                                                                    id='session_coach',
                                                                    placeholder="Coach's Name"
                                                                ),
                                                                width=4
                                                            )
                                                        ],
                                                        className='mb-3'
                                                    ),
                                                    dbc.Row(
                                                        [
                                                            dbc.Label("Football Program", width=2),
                                                            dbc.Col(
                                                                html.H3("Football Program",id='session_fbprogram',
                                                                          style={'border': '1px solid #ced4da',
                                                                                'padding': '0.5em', 
                                                                                'font-size': '16px',
                                                                                'height':'45px',
                                                                                'border-radius':'5px',
                                                                                'font-weight':'normal',
                                                                                'width':'145px',
                                                                                'display':'flex',
                                                                                'align-items':'center',
                                                                                'background-color': '#f0f0f0'}
                                                                )
                                                            )
                                                        ],
                                                        className='mb-3'
                                                    ),
                                                    dbc.Row(
                                                        [
                                                            dbc.Label("Age Group", width=2),
                                                            dbc.Col(
                                                                html.H3("Age Group",id='session_agegroup',
                                                                          style={'border': '1px solid #ced4da',
                                                                                'padding': '0.5em', 
                                                                                'font-size': '16px',
                                                                                'height':'45px',
                                                                                'border-radius':'5px',
                                                                                'font-weight':'normal',
                                                                                'width':'145px',
                                                                                'display':'flex',
                                                                                'align-items':'center',
                                                                                'background-color': '#f0f0f0'}
                                                                )
                                                            )
                                                        ],
                                                        className='mb-3'
                                                    ),
                                                    dbc.Row(
                                                        [
                                                            dbc.Label("Session Date", width=2),
                                                            dbc.Col(
                                                                dcc.DatePickerSingle(
                                                                    id="session_date",
                                                                    placeholder="Date",
                                                                    month_format = 'MMM Do, YY',
                                                                    display_format='YYYY-MM-DD'
                                                                ),
                                                                width=2
                                                            ),
                                                            dbc.Col(
                                                                html.H3("DOTW",id='session_dotw',
                                                                          style={'border': '1px solid #ced4da',
                                                                                'padding': '0.5em', 
                                                                                'font-size': '16px',
                                                                                'height':'45px',
                                                                                'border-radius':'5px',
                                                                                'font-weight':'normal',
                                                                                'width':'145px',
                                                                                'display':'flex',
                                                                                'align-items':'center'}
                                                                )
                                                            )
                                                        ],
                                                        className='mb-3'
                                                    ),
                                                    dbc.Row(
                                                        [
                                                            dbc.Label("Available Schedules", width=2),
                                                            dbc.Col(
                                                                dcc.Dropdown(
                                                                    id="session_schedule",
                                                                    placeholder="Time"
                                                                ),
                                                                width=4
                                                            ),
                                                        ],
                                                        className='mb-3'
                                                    ),
                                                    html.Div(
                                                        "New schedule input goes here",
                                                        id='session_newschedule'
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    dbc.Col(
                                            dbc.Button(
                                                'Submit',
                                                id='sessionsadd_submit',
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
                    ['Message here! Edit me please!'], id='sessionsadd_feedback_message'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/sessions',
                        id='sessionsadd_btn_modal'
                    )
                )
            ],
            centered=True,
            id='sessionsadd_successmodal',
            backdrop='static'
        )
    ]
)

@app.callback(
    [
        Output('session_schedule', 'options')
    ],
    [
        Input('url', 'pathname'),
        Input('session_date', 'date')
    ]
)
def sessionsadd_populateschedule(pathname, date):
    if pathname == '/sessions/sessionsadd' and date is not None:
       
        selected_date = datetime.strptime(date, '%Y-%m-%d')
        
      
        day_of_week = selected_date.strftime('%A')

        sql = """
        SELECT schedule_time, schedule_id
        FROM schedules
        WHERE schedule_dotw = %s
        """
        values = [day_of_week]
        cols = ['label', 'value']

        df = db.querydatafromdatabase(sql, values, cols)

        additional_option = [{'label':'Add new schedule', 'value':'new_schedule'}]
        schedule_options = sorted(additional_option + df.to_dict('records'), key=lambda x: (x['label'] != 'Add new schedule', x['label']))

        return [schedule_options]
    else:
        raise PreventUpdate


@app.callback(
    [
        Output('session_coach', 'options')
    ],
    [
        Input('url', 'pathname')
    ]
)
def sessionsadd_populatecoaches(pathname):
    if pathname == '/sessions/sessionsadd':
        sql = """
        SELECT CONCAT(coach_firstname, ' ', coach_lastname) AS label, coach_id as value
        FROM coaches;
        """
        values = []
        cols = ['label', 'value']

        df = db.querydatafromdatabase(sql, values, cols)

        coaches_options = df.to_dict('records')
        return [coaches_options]
    else:
        raise PreventUpdate
    
@app.callback(
    [
        Output('sessionsadd_alert','color'),
        Output('sessionsadd_alert','children'),
        Output('sessionsadd_alert','is_open'),
        Output('sessionsadd_successmodal','is_open'),
        Output('sessionsadd_feedback_message','children'),
        Output('sessionsadd_btn_modal','href')
    ],
    [
        Input('sessionsadd_submit', 'n_clicks'),
        Input('sessionsadd_btn_modal','n_clicks'),
    ],
    [
        State('session_coach','value'),
        State('session_date','date'),
        State('session_schedule','value'),
        State('newschedule_time','value'),
        State('url','search')
    ]
)
def sessionsadd_savesession(submitbtn, closebtn, session_coach, session_date, session_schedule, newschedule_time,search):
    ctx = dash.callback_context
   
    if newschedule_time is None:
      
        pass
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'sessionsadd_submit' and submitbtn:
           
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''
            feedbackmessage=''
            okay_href=''

          
            if not session_coach: 
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please choose a coach.'
            elif not session_date:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter a date.'
            elif not session_schedule:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please choose a schedule'
            else: 
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]

                if create_mode == 'add':
                    if session_schedule != 'new_schedule':
                        sql_session="""INSERT INTO trainingsession(
                            session_date,
                            schedule_id
                            )
                            VALUES(%s,%s)"""

                        values_session=[session_date, session_schedule]
                        db.modifydatabase(sql_session, values_session)


                        sql_coach="""INSERT INTO coachassignment(
                            session_id,
                            coach_id
                            )
                            VALUES((SELECT session_id FROM trainingsession WHERE session_date=%s and schedule_id=%s),%s)"""
                        values_coach=(session_date,session_schedule,session_coach)
                        db.modifydatabase(sql_coach, values_coach)
                    else:
                        sql_schedule="""INSERT INTO schedules(
                            schedule_time,
                            schedule_dotw
                            )
                            VALUES(%s,%s)"""
                        selected_date = datetime.strptime(session_date, '%Y-%m-%d')
                        day_of_week = selected_date.strftime('%A')
                        values_schedule=[newschedule_time,day_of_week]
                        db.modifydatabase(sql_schedule, values_schedule)

                        sql_session="""INSERT INTO trainingsession(
                            session_date,
                            schedule_id
                            )
                            VALUES(%s,(SELECT schedule_id FROM schedules WHERE schedule_time=%s and schedule_dotw=%s))"""
                        values_session=[session_date, newschedule_time, day_of_week]
                        db.modifydatabase(sql_session,values_session)

                        sql_coach="""INSERT INTO coachassignment(
                            session_id,
                            coach_id
                            )
                            VALUES((SELECT session_id FROM trainingsession WHERE session_date=%s and schedule_id=(SELECT schedule_id FROM schedules WHERE schedule_time=%s and schedule_dotw=%s)), %s)"""
                        values_coach=[session_date, newschedule_time, day_of_week, session_coach]
                        db.modifydatabase(sql_coach, values_coach)
                 
                    feedbackmessage = 'Session has been saved.'
                    okay_href='/sessions'
                    modal_open = True
                elif create_mode == 'edit':
                    pass
                else:
                    raise PreventUpdate

            return [alert_color, alert_text, alert_open, modal_open, feedbackmessage, okay_href]

        else: 
            raise PreventUpdate

    else:
        raise PreventUpdate