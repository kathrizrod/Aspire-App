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
        dbc.Row(
            dbc.Col(html.H2("Add A Coach"), width={"size": 6, "offset": 3}),
            className="mb-4"
        ),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            dbc.Alert(id="addcoach_alert", is_open=False),
                            dbc.Form(
                                [
                                    dbc.CardGroup(
                                        [
                                            dbc.Label("First Name", width=2),
                                            dbc.Col(
                                                dbc.Input(
                                                    type='text',
                                                    id="addcoach_firstname",
                                                    placeholder="Insert First Name",
                                                    style={"width": "100%"}
                                                ),
                                            ),
                                        ],
                                        className="mb-3"
                                    ),
                                    dbc.CardGroup(
                                        [
                                            dbc.Label("Middle Name", width=2),
                                            dbc.Col(
                                                dbc.Input(
                                                    type='text',
                                                    id="addcoach_middlename",
                                                    placeholder="Insert Middle Name",
                                                    style={"width": "100%"}
                                                ),
                                            ),
                                        ],
                                        className="mb-3"
                                    ),
                                    dbc.CardGroup(
                                        [
                                            dbc.Label("Last Name", width=2),
                                            dbc.Col(
                                                dbc.Input(
                                                    type='text',
                                                    id="addcoach_lastname",
                                                    placeholder="Insert Last Name",
                                                    style={"width": "100%"}
                                                ),
                                            ),
                                        ],
                                        className="mb-3"
                                    ),
                                    dbc.CardGroup(
                                        [
                                            dbc.Label("Age Group", width=2),
                                            dcc.Dropdown(
                                                id="addcoach_agegroup",
                                                placeholder="Select or type age group",
                                                options=[],  # Initially empty, to be populated dynamically
                                                multi=False,  # Set to True if you want to allow multiple selections
                                                style={"width": "100%"}  # Make dropdown full-width
                                            ),
                                        ],
                                        className="mb-3"
                                    ),
                                     dbc.CardGroup(
                                        [
                                            dbc.Label("Program", width=2),
                                            dcc.Dropdown(
                                                id="addcoach_program",
                                                placeholder="Select or type program",
                                                options=[],  # Initially empty, to be populated dynamically
                                                multi=False,  # Set to True if you want to allow multiple selections
                                                style={"width": "100%"}  # Make dropdown full-width
                                            ),
                                        ],
                                        className="mb-3"
                                    ),
                                ]
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.Button("Submit", id="addcoach_submit", n_clicks=0), width=6),
                                    dbc.Col(dbc.Button("Return", href="/coaches"), width=6),
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
                dbc.ModalBody("The coach was successfully added."),
                dbc.ModalFooter(
                    dbc.Button("Proceed", href="/coaches")
                )
            ],
            centered=True,
            id="addcoach_successmodal",
            backdrop='static'
        )
    ],
    className="mt-5",  # Adjust the top margin for centering
)

@app.callback(
    [Output('addcoach_agegroup', 'options')],
    [Input('url', 'pathname')]
)
def playeradd_populateagegroup(pathname):
    if pathname == '/coaches/addcoach':
        sql = """
        SELECT group_name AS label, group_id AS value
        FROM agegroups;
        """
        values = []
        cols = ['label', 'value']

        df = db.querydatafromdatabase(sql, values, cols)
        agegroup_options = df.to_dict('records')
        return [agegroup_options]
    else:
        raise PreventUpdate

@app.callback(
    [Output('addcoach_program', 'options')],
    [Input('url', 'pathname')]
)
def playeradd_populateprogram(pathname):
    if pathname == '/coaches/addcoach':
        sql = """
        SELECT program_name AS label, program_id AS value
        FROM fbprograms;
        """
        values = []
        cols = ['label', 'value']

        df = db.querydatafromdatabase(sql, values, cols)
        program_options = df.to_dict('records')
        return [program_options]
    else:
        raise PreventUpdate

@app.callback(
    [
        # dbc.Alert Properties
        Output('addcoach_alert', 'color'),
        Output('addcoach_alert', 'children'),
        Output('addcoach_alert', 'is_open'),
        # dbc.Modal Properties
        Output('addcoach_successmodal', 'is_open'),
    ],
    [
        # For buttons, the property n_clicks 
        Input('addcoach_submit', 'n_clicks'),
    ],
    [
        # The values of the fields are States 
        # They are required in this process but they 
        # do not trigger this callback
        State('addcoach_firstname', 'value'),
        State('addcoach_middlename', 'value'),
        State('addcoach_lastname', 'value'),
        State('addcoach_agegroup', 'value'),
        State('addcoach_program', 'value')
    ]
)
def coach_add(submitbtn, addcoach_firstname, addcoach_middlename, addcoach_lastname, addcoach_agegroup, addcoach_program):
    ctx = dash.callback_context
    # The ctx filter -- ensures that only a change in url will activate this callback
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'addcoach_submit' and submitbtn:
            # the submitbtn condition checks if the callback was indeed activated by a click
            # and not by having the submit button appear in the layout

            # Set default outputs
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''

            # We need to check inputs
            if not addcoach_firstname: # If title is blank, not title = True
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter first name of the coach.'
            elif not addcoach_middlename:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter middle name of the coach.'
            elif not addcoach_lastname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter last name of the coach.'
            elif not addcoach_agegroup:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter age group assigned to the coach.'
            else: # all inputs are valid
                # Add the data into the db

                sql = """ INSERT INTO coaches(
                    coach_firstname,
                    coach_middlename,
                    coach_lastname,
                    group_id,
                    program_id
                    )
                    VALUES(%s, %s, %s, %s, %s)"""
            
                values = [addcoach_firstname, addcoach_middlename, addcoach_lastname, addcoach_agegroup, addcoach_program]

                db.modifydatabase(sql, values)
                modal_open = True

            return [alert_color, alert_text, alert_open, modal_open]

        else: # Callback was not triggered by desired triggers
            raise PreventUpdate

    else:
        raise PreventUpdate
