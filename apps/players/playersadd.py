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

@app.callback(
    Output('player_newparent', 'children'),
    [Input('player_parent', 'value')]
)
def playersadd_addnewparent(newparent):
    if newparent == 'new_parent':
        newinput = dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Label("First Name", width=4),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='parent_firstname',
                                placeholder="First Name"
                            ),
                            width=8
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Middle Name", width=4),
                        dbc.Col(
                            dbc.Input(
                                id='parent_middlename',
                                placeholder='Middle Name'
                            ),
                            width=8
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Last Name", width=4),
                        dbc.Col(
                            dbc.Input(
                                id='parent_lastname',
                                placeholder='Last Name'
                            ),
                            width=8
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Contact Number", width=4),
                        dbc.Col(
                            dbc.Input(
                                id='parent_contact',
                                placeholder='Contact Number'
                            ),
                            width=8
                        )
                    ],
                    className='mb-3'
                ),
            ]
        )
    else:
        newinput = dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Label("First Name", width=4),
                        dbc.Col(
                            dbc.Input(
                                type='text',
                                id='parent_firstname',
                                placeholder="First Name",
                                disabled=True
                            ),
                            width=8
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Middle Name", width=4),
                        dbc.Col(
                            dbc.Input(
                                id='parent_middlename',
                                placeholder='Middle Name',
                                disabled=True
                            ),
                            width=8
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Last Name", width=4),
                        dbc.Col(
                            dbc.Input(
                                id='parent_lastname',
                                placeholder='Last Name',
                                disabled=True
                            ),
                            width=8
                        )
                    ],
                    className='mb-3'
                ),
                dbc.Row(
                    [
                        dbc.Label("Contact Number", width=4),
                        dbc.Col(
                            dbc.Input(
                                id='parent_contact',
                                placeholder='Contact Number',
                                disabled=True
                            ),
                            width=8
                        )
                    ],
                    className='mb-3'
                ),
            ]
        )
    return newinput



layout = html.Div(
    [
        html.H2('Add Player Details'),  
        html.Hr(),
        dbc.Alert(id='playersadd_alert', is_open=False), 
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Player Information",style={'font-weight': '600'}),
                            dbc.CardBody(
                                [
                                    dbc.Form(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Label("First Name", width=4),
                                                    dbc.Col(
                                                        dbc.Input(
                                                            type='text',
                                                            id='player_firstname',
                                                            placeholder="First Name"
                                                        ),
                                                        width=8
                                                    )
                                                ],
                                                className='mb-3'
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Label("Middle Name", width=4),
                                                    dbc.Col(
                                                        dbc.Input(
                                                            id='player_middlename',
                                                            placeholder='Middle Name'
                                                        ),
                                                        width=8
                                                    )
                                                ],
                                                className='mb-3'
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Label("Last Name", width=4),
                                                    dbc.Col(
                                                        dbc.Input(
                                                            id='player_lastname',
                                                            placeholder='Last Name'
                                                        ),
                                                        width=8
                                                    )
                                                ],
                                                className='mb-3'
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Label("Gender", width=4),
                                                    dbc.Col(
                                                        dcc.Dropdown(
                                                            id='player_gender',
                                                            placeholder='Gender'
                                                        ),
                                                        width=8
                                                    )
                                                ],
                                                className='mb-3'
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Label("Birth Date", width=4),
                                                    dbc.Col(
                                                        dcc.DatePickerSingle(
                                                            id='player_birthday',
                                                            placeholder='Birth Date',
                                                            month_format='MMM Do, YY',
                                                            display_format='YYYY-MM-DD'
                                                        ),
                                                        width=8,
                                                    )
                                                ],
                                                className='mb-3'
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Label("Football Program", width=4),
                                                    dbc.Col(
                                                        dcc.Dropdown(
                                                            id='player_fbprogram',
                                                            placeholder='Football Program'
                                                        ),
                                                        width=8,
                                                    )
                                                ],
                                                className='mb-3'
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Label("Age Group", width=4),
                                                    dbc.Col(
                                                        dcc.Dropdown(
                                                            id='player_agegroup',
                                                            placeholder='Age Group'
                                                        ),
                                                        width=8
                                                    )
                                                ],
                                                className='mb-3'
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                    width=6
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Parent/Guardian Information", style={'font-weight': '600'}),
                            dbc.CardBody(
                                [
                                    dbc.Form(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Label("Full Name", width=4),
                                                    dbc.Col(
                                                        dcc.Dropdown(
                                                            id='player_parent',
                                                            placeholder='Parent/Guardian'
                                                        ),
                                                        width=8
                                                    )
                                                ],
                                                className='mb-3'
                                            ),
                                            html.Div(
                                                "New parent/guardian input goes here",
                                                id = 'player_newparent'
                                            )
                                        ]
                                    )
                                ]
                            ),
                        ]
                    ),
                    width=6
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button(
                        "Submit",
                        id='playersadd_submit',
                        n_clicks=0,
                        className='mr-2', 
                    )
                ),
                dbc.Col(
                    dbc.Button(
                        "Back",
                        href='/players',
                        color='secondary',
                    )
                )
            ],
            className="justify-content-end",
            style={'margin-top': '20px'},  
        ),
        dbc.Modal(  
            [
                dbc.ModalHeader(
                    html.H4('Save Success')
                ),
                dbc.ModalBody('Player has been saved.'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/players',  
                    )
                )
            ],
            centered=True,
            id='playersadd_successmodal',
            backdrop='static'  
        )
    ]
)

@app.callback(
    [
        Output('player_gender', 'options')
    ],
    [
        Input('url', 'pathname')
    ]
)
def playeradd_populategender(pathname):
    if pathname == '/players/playersadd':
        gender_options=[
            {'label': "Male", 'value': "male"},
            {'label': "Female", 'value': "female"}
        ]
        cols = ['label', 'value']
        return [gender_options]
    else:
        
        raise PreventUpdate

@app.callback(
    [
        Output('player_fbprogram', 'options')
    ],
    [
        Input('url', 'pathname')
    ]
)
def playeradd_populatefbprograms(pathname):
    if pathname == '/players/playersadd':
        sql = """
        SELECT program_name as label, program_id as value
        FROM fbprograms
        """
        values = []
        cols = ['label', 'value']

        df = db.querydatafromdatabase(sql, values, cols)
        fbprograms_options = df.to_dict('records')
        return [fbprograms_options]
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('player_agegroup', 'options')
    ],
    [
        Input('url', 'pathname')
    ]
)
def playeradd_populateagegroups(pathname):
    if pathname == '/players/playersadd':
        sql = """
        SELECT group_name as label, group_id as value
        FROM agegroups
        """
        values = []
        cols = ['label', 'value']

        df = db.querydatafromdatabase(sql, values, cols)

        agegroups_options = df.to_dict('records')
        return [agegroups_options]
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('player_parent', 'options')
    ],
    [
        Input('url', 'pathname')
    ]
)
def playeradd_populateparents(pathname):
    if pathname == '/players/playersadd':
        sql = """
        SELECT CONCAT(parent_lastname, ', ', parent_firstname, ' ', parent_middlename) AS label, parent_id as value
        FROM parents;
        """
        values = []
        cols = ['label', 'value']

        df = db.querydatafromdatabase(sql, values, cols)

        additional_option = [{'label':'Add new parent/guardian', 'value':'new_parent'}]
        parents_options = sorted(additional_option + df.to_dict('records'), key=lambda x: (x['label'] != 'Add new parent/guardian', x['label']))
        return [parents_options]
    else:
        raise PreventUpdate

@app.callback(
    [
       
        Output('playersadd_alert', 'color'),
        Output('playersadd_alert', 'children'),
        Output('playersadd_alert', 'is_open'),
        
        Output('playersadd_successmodal', 'is_open')
    ],
    [
      
        Input('playersadd_submit', 'n_clicks')
    ],
    [
       
        State('player_firstname', 'value'),
        State('player_middlename', 'value'),
        State('player_lastname', 'value'),
        State('player_gender', 'value'),
        State('player_birthday', 'date'),
        State('player_fbprogram', 'value'),
        State('player_agegroup', 'value'),
        State('player_parent', 'value'),
        State('parent_firstname', 'value'),
        State('parent_middlename','value'),
        State('parent_lastname','value'),
        State('parent_contact','value'),
        State('url','search')
    ]
)
def playersadd_saveprofile(submitbtn, player_firstname, player_middlename, player_lastname, player_gender, player_birthday, player_fbprogram, player_agegroup, player_parent, parent_firstname, parent_middlename, parent_lastname, parent_contact, search):
    ctx = dash.callback_context
   
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'playersadd_submit' and submitbtn:
          
            alert_open = False
            modal_open = False
            alert_color = ''
            alert_text = ''

        
            if not player_firstname: 
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter first name.'
            elif not player_middlename:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter middle name.'
            elif not player_lastname:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter last name.'
            elif not player_gender:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter gender.'
            elif not player_birthday:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter birthday'
            elif not player_fbprogram:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter Football Program'
            elif not player_agegroup:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter Age Group'
            elif not player_parent:
                alert_open = True
                alert_color = 'danger'
                alert_text = 'Check your inputs. Please enter Parent'
            else: 
                parsed = urlparse(search)
                create_mode = parse_qs(parsed.query)['mode'][0]

                if create_mode == 'add':
                    if player_parent == 'new_parent':
                        sql_parent = """INSERT INTO parents(
                            parent_firstname,
                            parent_middlename,
                            parent_lastname,
                            parent_contact
                            )
                            VALUES(%s, %s, %s, %s)"""
                        values_parent = [parent_firstname, parent_middlename, parent_lastname, parent_contact]
                        db.modifydatabase(sql_parent, values_parent)

                        sql_player = """INSERT INTO players(
                            player_firstname,
                            player_middlename,
                            player_lastname,
                            player_gender,
                            player_birthday,
                            program_id,
                            group_id,
                            parent_id
                        )
                        VALUES(%s, %s, %s, %s, %s, %s, %s, 
                            (SELECT parent_id FROM parents WHERE parent_firstname=%s AND parent_middlename=%s AND parent_lastname=%s))"""
                        values_player = [player_firstname, player_middlename, player_lastname, player_gender, player_birthday, player_fbprogram, player_agegroup, parent_firstname, parent_middlename, parent_lastname]
                        db.modifydatabase(sql_player, values_player)
                    else:
                        sql = """ INSERT INTO players(
                            player_firstname,
                            player_middlename,
                            player_lastname,
                            player_gender,
                            player_birthday,
                            program_id,
                            group_id,
                            parent_id
                            )
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
                
                        values = [player_firstname, player_middlename, player_lastname, player_gender, player_birthday, player_fbprogram, player_agegroup, player_parent]

                        db.modifydatabase(sql, values)

                  
                    modal_open = True
                elif create_mode == 'profile':
                    pass
                else:
                    raise PreventUpdate

            return [alert_color, alert_text, alert_open, modal_open]

        else: 
            raise PreventUpdate

    else:
        raise PreventUpdate
