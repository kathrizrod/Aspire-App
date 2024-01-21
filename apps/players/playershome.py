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
    [
        Output('playershome_playerlist','children')
    ],
    [
        Input('url','pathname'),
        Input('playershome_lastnamefilter','value'),
        Input('playershome_givennamefilter','value'),
        Input('playershome_fbprogramfilter','value'),
        Input('playershome_agegroupfilter','value')
    ]
)
def playershome_loadplayerlist(pathname, searchterm_lastname, searchterm_givenname, filter_fbprogram, filter_agegroup):
    if pathname == '/players':
        sql = """SELECT player_lastname, CONCAT(player_firstname, ' ', player_middlename) AS player_givenname, program_name, group_name, player_id
        FROM players p
            INNER JOIN fbprograms f ON p.program_id = f.program_id
            INNER JOIN agegroups a ON p.group_id = a.group_id
        """

        values = []
        cols = ['Last Name','Given Name','Football Program', 'Age Group','ID']

        if searchterm_lastname:
            sql += " AND player_lastname ILIKE %s"
            values += [f"%{searchterm_lastname}%"]

        if searchterm_givenname:
            if 'WHERE' in sql:
                sql += " AND CONCAT(player_firstname, ' ', player_middlename) ILIKE %s"
            else:
                sql += " WHERE CONCAT(player_firstname, ' ', player_middlename) ILIKE %s"
            values += [f"%{searchterm_givenname}%"]

        if filter_agegroup:
            if isinstance(filter_agegroup, str):
                filter_agegroup = [filter_agegroup]
            filter_agegroup_tuple = tuple(filter_agegroup)
            if len(filter_agegroup_tuple)==1:
                sql += " AND group_name ILIKE %s"
                values += [filter_agegroup_tuple[0]]
            else:
                sql += f" AND group_name IN {filter_agegroup_tuple}"

        if filter_fbprogram:
            if isinstance(filter_fbprogram, str):
                filter_fbprogram = [filter_fbprogram]
            filter_fbprogram_tuple = tuple(filter_fbprogram)
            if len(filter_fbprogram_tuple)==1:
                sql += " AND program_name ILIKE %s"
                values += [filter_fbprogram_tuple[0]]
            else:
                sql += f" AND program_name IN {filter_fbprogram_tuple}"

        sql += " AND player_isdeleted = FALSE ORDER BY player_lastname"
        
        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            buttons = []
            for player_id in df['ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Profile', href=f'players/playersprofile?mode=profile&id={player_id}',
                           size='sm', color='warning'),
                           style={'text-align':'center'}
                    )
                ]
            df['Profile']=buttons

            df = df[['Last Name','Given Name','Football Program', 'Age Group', 'Profile']]
            
            total_row = df.shape[0]
            total_row_html = html.Div(
                dbc.Table.from_dataframe(pd.DataFrame({'Total:':[f'{total_row} Player/s']}),size='sm'),
                style={'text-align':'right'}
            )
            
            table = [
                html.Div(
                    dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm'),
                    style={'height':'400px','overflowY':'scroll'}
                ),
                total_row_html
            ]
            return[table]
        else:
            return["No records to display"]

    else:
        raise PreventUpdate

layout = html.Div(
    [
        html.H2('Players'),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.Div(
                            [
                                dbc.Button(
                                    "Add Player", color="secondary",
                                    href='/players/playersadd?mode=add'
                                )
                            ]
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                html.H4('Find Players'),
                                html.Div(
                                    dbc.Form(
                                        dbc.Row(
                                            [
                                                dbc.Label("Search Player", width=1),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id="playershome_lastnamefilter",
                                                        placeholder='Last Name'
                                                    ),
                                                    width=3
                                                ),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id="playershome_givennamefilter",
                                                        placeholder='Given Name'
                                                    ),
                                                    width=3
                                                ),
                                            ],
                                            className = 'mb-3'
                                        )
                                    )
                                ),
                                html.Div(
                                    dbc.Form(
                                        dbc.Row(
                                            [dbc.Label("Filter", width=1),
                                            dbc.Col(
                                                dcc.Dropdown(
                                                    id='playershome_fbprogramfilter',
                                                    placeholder='Football Program',
                                                    multi=True
                                                ),
                                                width=3
                                            ),
                                            dbc.Col(
                                                dcc.Dropdown(
                                                    id='playershome_agegroupfilter',
                                                    placeholder = 'Age Group',
                                                    multi=True
                                                ),
                                                width=3
                                            ),
                                            dbc.Col(
                                                dbc.Button(
                                                    'Clear',
                                                    id = 'filter_reset',
                                                    color='secondary',
                                                    n_clicks=0
                                                )
                                            )]
                                        )
                                    )
                                ),
                                html.Hr(),
                                html.Div(
                                    [
                                        dbc.Col(
                                            "Table of players goes here",
                                            id='playershome_playerlist'
                                        ),
                                    ]
                                ),
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

@app.callback(
    [
        Output('playershome_fbprogramfilter','options')
    ],
    [
        Input('url','pathname')
    ]
)
def playerhome_populatefbprograms(pathname):
    if pathname == '/players':
        sql = """
        SELECT program_name as label, program_name as value
        FROM fbprograms
        """
        values = []
        cols = ['label','value']

        df = db.querydatafromdatabase(sql, values, cols)
        fbprograms_options = df.to_dict('records')
        return [fbprograms_options]
    else:
        raise PreventUpdate
     
@app.callback(
    [
        Output('playershome_agegroupfilter','options')
    ],
    [
        Input('url','pathname')
    ]
)
def playerhome_populateagegroups(pathname):
    if pathname == '/players':
        sql = """
        SELECT group_name as label, group_name as value
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
        Output('playershome_fbprogramfilter', 'value'),
        Output('playershome_agegroupfilter', 'value'),
        Output('playershome_lastnamefilter','value'),
        Output('playershome_givennamefilter','value')
    ],
    [
        Input('filter_reset', 'n_clicks')
    ]
)
def reset_filters(n_clicks):
    if n_clicks > 0:
        return None, None, None, None  
    else:
        return dash.no_update, dash.no_update 
    

    
    