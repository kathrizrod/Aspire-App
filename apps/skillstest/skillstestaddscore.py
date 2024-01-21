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
        dbc.Row(
            dbc.Col(html.H2("Add Player Score"), width={"size": 6, "offset": 3}),
            className="mb-4"
        ),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            dbc.Alert(id="addscore_alert", is_open=False),
                            dbc.Form(
                                [
                                    dbc.CardGroup(
                                        [
                                            dbc.Label("Player Name"),
                                            dcc.Dropdown(
                                                id="player_name",
                                                placeholder="Select or type player name",
                                                options=[],  
                                                multi=False, 
                                                style={"width": "100%"}  
                                            ),
                                        ],
                                        className="mb-3"
                                    ),

                                    dbc.CardGroup(
                                        [
                                            dbc.Label("Coach"),
                                            dcc.Dropdown(
                                                id="player_coach",
                                                placeholder="Select or type coach name",
                                                options=[], 
                                                style={"width": "100%"}  
                                            ),
                                        ],
                                        className="mb-3"
                                    ),
                                    dbc.CardGroup(
                                        [
                                            dbc.Label("Date"),
                                            dcc.DatePickerSingle(
                                                id='skill_date',
                                                placeholder='Select date',
                                                month_format='MMM Do, YY',
                                                display_format='YYYY-MM-DD',
                                                style={"width": "100%"} 
                                            ),
                                        ],
                                        className="mb-3"
                                    ),
                                    dbc.CardGroup(
                                        [
                                            dbc.Label("Score"),
                                            dbc.Input(
                                                type='text',
                                                id="player_score",
                                                placeholder="Enter score",
                                                style={"width": "100%"}  
                                            ),
                                        ],
                                        className="mb-3"
                                    ),
                                ]
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.Button("Submit", id="addscore_submit", n_clicks=0), width=6),
                                    dbc.Col(dbc.Button("Return", id='addscore_return', n_clicks=0, color='secondary'), width=6),
                                ],
                                className="mb-3"
                            )
                        ]
                    )
                ),
                width={"size": 6, "offset": 3},
            ),
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(html.H4('Save success!')),
                dbc.ModalBody("The Skills Test was successfully added."),
                dbc.ModalFooter(
                    dbc.Button("Proceed", id='addscore_proceed')
                )
            ],
            centered=True,
            id="addscore_successmodal",
            backdrop='static'
        )
    ],
    className="mt-5", 
)


@app.callback(
    [Output('player_name', 'options')],
    [Input('url', 'pathname')]
)
def playeradd_populateplayers(pathname):
    if pathname == '/skillstest/skillstestaddscore':
        sql = """
        SELECT player_firstname || ' ' || player_lastname AS label, player_id AS value
        FROM players;
        """
        values = []
        cols = ['label', 'value']

        df = db.querydatafromdatabase(sql, values, cols)
        players_options = df.to_dict('records')
        return [players_options]
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('player_coach', 'options')
    ],
    [
        Input('url', 'pathname')
    ]
)
def playeradd_populatecoach(pathname):
    if pathname == '/skillstest/skillstestaddscore':
        sql = """
        SELECT CONCAT(coach_firstname, ' ', coach_firstname) AS label, coach_id as value
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
      
        Output('addscore_alert', 'color'),
        Output('addscore_alert', 'children'),
        Output('addscore_alert', 'is_open'),
       
        Output('addscore_successmodal', 'is_open'),
        Output('addscore_return', 'href')
    ],
    [
        
        Input('addscore_submit', 'n_clicks'),
        Input('addscore_return', 'n_clicks')
    ],
    [
       
        State('player_name', 'value'),
        State('player_coach', 'value'),
        State('skill_date', 'date'),
        State('player_score', 'value'),
        State('url', 'search')
    ]
)
def add_playerscore(submitbtn, returnbtn, player_name, player_coach, skill_date, player_score, search):
    ctx = dash.callback_context
  
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'addscore_submit' and submitbtn:
           
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''

          
            if not player_name: 
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter name of player.'
            elif not player_coach:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter name of coach for the skills test.'
            elif not skill_date:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter date recorded.'
            elif not player_score:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter score of player for the skills test.'
            else:

                parsed = urlparse(search)
                skill_id = parse_qs(parsed.query)['id'][0]
                bool_entry = False

                sql = """INSERT INTO playerscore(player_id, skill_id, coach_id, test_date, score_skill, playerscore_isdeleted)
                VALUES (%s, %s, %s, %s, %s,%s)
                """
            
                values = [player_name, skill_id, player_coach, skill_date, player_score, bool_entry]

                db.modifydatabase(sql, values)

                modal_open = True
                return_href = f'/skillstest/skillstestdetails?mode=edit&id={skill_id}'
                
                return [alert_color, alert_text, alert_open, modal_open, return_href]
        
        elif eventid == 'addscore_return' and returnbtn:
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''

            parsed = urlparse(search)
            skill_id = parse_qs(parsed.query)['id'][0]

            return_href = f'/skillstest/skillstestdetails?mode=edit&id={skill_id}'

            return [alert_color, alert_text, alert_open, modal_open, return_href]

        else:
            raise PreventUpdate

    else:
        raise PreventUpdate

@app.callback(
    [
        Output('addscore_proceed', 'href')
    ],
    [
        Input('url','search')
    ]
)
def skillstest_gethref(search):

    parsed = urlparse(search)
    skillid = parse_qs(parsed.query)['id'][0]
    href = f'/skillstest/skillstestdetails?mode=edit&id={skillid}'
    
    return [href]