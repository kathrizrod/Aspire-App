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
            dbc.Col(html.H2("Add Skills Test Details"), width={"size": 6, "offset": 3}),
            className="mb-4"
        ),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            dbc.Alert(id="skillstestprofile_alert", is_open=False),
                            dbc.Form(
                                [
                                    dbc.CardGroup(
                                        [
                                            dbc.Label("Name", width=2),
                                            dbc.Col(
                                                dbc.Input(
                                                    type='text',
                                                    id="skillstest_name",
                                                    placeholder="Skills Test Name",
                                                    style={"width": "100%"}
                                                ),
                                            ),
                                        ],
                                        className="mb-3"
                                    ),
                                    dbc.CardGroup(
                                        [
                                            dbc.Label("Description", width=2),
                                            dbc.Col(
                                                dbc.Input(
                                                    type='text',
                                                    id="skillstest_desc",
                                                    placeholder="Description",
                                                    style={"width": "100%"}
                                                ),
                                            ),
                                        ],
                                        className="mb-3"
                                    ),
                                    dbc.CardGroup(
                                        [
                                            dbc.Label("Instructions", width=2),
                                            dbc.Col(
                                                dbc.Input(
                                                    type='text',
                                                    id="skillstest_ins",
                                                    placeholder="Instructions",
                                                    style={"width": "100%"}
                                                ),
                                            ),
                                        ],
                                        className="mb-3"
                                    ),
                                    dbc.CardGroup(
                                        [
                                            dbc.Label("Metric", width=2),
                                            dbc.Col(
                                                dbc.Input(
                                                    type='text',
                                                    id="skillstest_metric",
                                                    placeholder="Metric",
                                                    style={"width": "100%"}
                                                ),
                                            ),
                                        ],
                                        className="mb-3"
                                    ),
                                ]
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.Button("Submit", id="addskillstest_submit", n_clicks=0), width=6),
                                    dbc.Col(dbc.Button("Return", href="/skillstest", color='secondary'), width=6),
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
                    dbc.Button("Proceed", href="/skillstest")
                )
            ],
            centered=True,
            id="skillstestprofile_successmodal",
            backdrop='static'
        )
    ],
    className="mt-5",  
)

@app.callback(
    [
      
        Output('skillstestprofile_alert', 'color'),
        Output('skillstestprofile_alert', 'children'),
        Output('skillstestprofile_alert', 'is_open'),
       
        Output('skillstestprofile_successmodal', 'is_open'),
    ],
    [
        
        Input('addskillstest_submit', 'n_clicks'),
    ],
    [
       
        State('skillstest_name', 'value'),
        State('skillstest_desc', 'value'),
        State('skillstest_ins', 'value'),
        State('skillstest_metric', 'value')
    ]
)
def skillstest_add(submitbtn, skillstest_name, skillstest_desc, skillstest_ins, skillstest_metric):
    ctx = dash.callback_context
 
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'addskillstest_submit' and submitbtn:
           
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''

       
            if not skillstest_name: 
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter name of skills test.'
            elif not skillstest_desc:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter description of skills test.'
            elif not skillstest_ins:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter instructions for skill test.'
            elif not skillstest_metric:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter metric to be used for skill test.'
            else: 
                sql = """ INSERT INTO skillstest(
                    skill_name,
                    skill_desc,
                    skill_ins,
                    skill_scoreunit
                    )
                    VALUES(%s, %s, %s, %s)"""
            
                values = [skillstest_name, skillstest_desc, skillstest_ins, skillstest_metric]

                db.modifydatabase(sql, values)

                modal_open = True

            return [alert_color, alert_text, alert_open, modal_open]

        else:
            raise PreventUpdate

    else:
        raise PreventUpdate
