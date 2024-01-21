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


def create_table_from_dataframe(df, actions=None):
    if df.shape[0]:
        if actions:
            for action in actions:
                df[action['column']] = action['buttons']

        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
        return [table]
    else:
        return ["No records to display"]


layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Return", color="secondary", href='/skillstest'),
                    width=2
                )
            ],
            className='mb-3'
        ),
        html.H2('Skills Test Results'),
        html.Hr(),
        html.Div(
            [
                dbc.Col(
                    "Table of skills test info goes here",
                    id='skillstest_info',
                    style={'text-align': 'center'}
                )
            ]
        ),
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H5("Player Scores"),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button("Add Player Score", color="secondary", id='skillstest_addscorehref'),
                                    width=2
                                ),
                                dbc.Col(
                                    dbc.Button("Delete Skills Test", color="danger", id='skillstest_delete', n_clicks=0),
                                    width=2
                                )
                            ],
                            className='mb-3'
                        ),
                        dbc.Row(
                            [
                                dbc.Label("Search", width=1),
                                dbc.Col(
                                    dbc.Input(id='player_name_search', type='text', placeholder='By Player Name'),
                                    width=5
                                )
                            ],
                            className='mb-3'
                        ),
                        dbc.Row(
                            [
                                dbc.Label("Sort By:", width=1),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='sorting_dropdown',
                                        options=[
                                            {'label': 'Player Name', 'value': 'Player Name'},
                                            {'label': 'Score', 'value': 'Score'}
                                        ],
                                        value='Player Name',  
                                        clearable=False,
                                        style={'width': '100%'}
                                    ),
                                    width=3
                                )
                            ],
                            className='mb-3'
                        ),
                        html.Div("Table of player scores for skills test goes here", id='skillstest_playerscore', style={'text-align': 'center'}),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(html.H4('Delete Skills Test')),
                                dbc.ModalBody("Are you sure you want to delete skills test?", style={'text-align': 'center'}),
                                dbc.ModalFooter(
                                    [
                                        dbc.Button("Proceed", id='skillstest_godelete', n_clicks=0),
                                        dbc.Button("No", href="/skillstest")
                                    ]
                                )
                            ],
                            centered=True,
                            id="skillstestdelete_successmodal",
                            backdrop='static'
                        )
                    ]
                )
            ]
        ),
        html.Div(
            [
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(id='score_histogram'),
                            width=12
                        )
                    ]
                )
            ]
        )
    ]
)


@app.callback(
    [Output('skillstest_info', 'children')],
    [Input('url', 'pathname')],
    [State('url', 'search')]
)
def skillstest_getdetails(pathname, search):
    if pathname == "/skillstest/skillstestdetails":
        sql = """ SELECT skill_name, skill_desc, skill_ins, skill_scoreunit
            FROM skillstest
            WHERE skillstest.skill_id = %s
        """

        parsed = urlparse(search)
        skillid = parse_qs(parsed.query)['id'][0]
        values = [skillid]
        cols = ['Skills Test', 'Description', 'Instructions', 'Metric']

        df = db.querydatafromdatabase(sql, values, cols)
        return create_table_from_dataframe(df)
    else:
        raise PreventUpdate


@app.callback(
    [Output('skillstest_addscorehref', 'href')],
    [Input('url', 'pathname')],
    [State('url', 'search')]
)
def skillstest_gethref(pathname, search):
    if pathname == "/skillstest/skillstestdetails":
        parsed = urlparse(search)
        skillid = parse_qs(parsed.query)['id'][0]
        href = f'/skillstest/skillstestaddscore?mode=add&id={skillid}'
        return [href]
    else:
        raise PreventUpdate


@app.callback(
    [Output('skillstestdelete_successmodal', 'is_open')],
    [Input('skillstest_delete', 'n_clicks')]
)
def skillstest_delete(deletebtn):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'skillstest_delete' and deletebtn:
            return [True]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(
    [Output('skillstest_godelete', 'href')],
    [Input('skillstest_godelete', 'n_clicks')],
    [Input('url', 'search')]
)
def skillstest_delete(deletebtn, search):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'skillstest_godelete' and deletebtn:
            sql = """ UPDATE skillstest
                SET skill_isdeleted = %s
                WHERE skillstest.skill_id = %s
            """

            parsed = urlparse(search)
            skillid = parse_qs(parsed.query)['id'][0]
            values = [True, skillid]

            db.modifydatabase(sql, values)

            return_href = "/skillstest"
            return [return_href]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(
    [Output('skillstest_playerscore', 'children')],
    [Input('url', 'pathname'), Input('url', 'search'), Input('player_name_search', 'value'), Input('sorting_dropdown', 'value')]
)
def skillstest_loadplayersscore(pathname, search, searchterm, sortby):
    if pathname == "/skillstest/skillstestdetails":
        sql = """
            SELECT
                players.player_firstname || ' ' || players.player_lastname AS player_name,
                agegroups.group_name AS age_group,
                fbprograms.program_name AS program,
                coaches.coach_firstname || ' ' || coaches.coach_lastname AS coach_assigned,
                playerscore.test_date AS date_recorded,
                playerscore.score_skill AS test_score,
                playerscore.score_id
            FROM
                playerscore
            JOIN skillstest ON playerscore.skill_id = skillstest.skill_id
            JOIN players ON playerscore.player_id = players.player_id
            JOIN agegroups ON players.group_id = agegroups.group_id
            JOIN fbprograms ON players.program_id = fbprograms.program_id
            JOIN coaches ON playerscore.coach_id = coaches.coach_id
            WHERE
                playerscore.skill_id = %s AND playerscore.playerscore_isdeleted = FALSE
        """

        parsed = urlparse(search)
        skillid = parse_qs(parsed.query)['id'][0]

        values = [skillid]
        cols = ['Player Name', 'Age Group', 'Program', 'Coach', 'Date', 'Score', 'ID']

        if searchterm:
            sql += " AND players.player_firstname || ' ' || players.player_lastname ILIKE %s"
            values += [f"%{searchterm}%"]
        
        if sortby == 'Player Name':
            sql += "\nORDER BY player_name ASC"
        elif sortby == 'Score':
            sql += "\nORDER BY test_score DESC"

        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            buttons = []
            for score_id in df['ID']:
                buttons.append(
                    html.Div(
                        dbc.Button('Delete', href=f'/skillstest/deleteplayerscore?mode=edit&id={score_id}', n_clicks=0, size='sm', color='warning'),
                        style={'text-align': 'center'}
                    )
                )
            df['Delete?'] = buttons

            df = df[['Player Name', 'Age Group', 'Program', 'Coach', 'Date', 'Score', 'Delete?']]

        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')

        return [table]
    
    else:
        raise PreventUpdate


@app.callback(
    Output('score_histogram', 'figure'),
    [Input('url', 'pathname'), Input('url', 'search')]
)
def update_histogram(pathname, search):
    if pathname == "/skillstest/skillstestdetails":
        sql = """
            SELECT
                playerscore.score_skill
            FROM
                playerscore
            WHERE
                playerscore.skill_id = %s AND playerscore.playerscore_isdeleted = FALSE
        """

        parsed = urlparse(search)
        skillid = parse_qs(parsed.query)['id'][0]

        values = [skillid]

        scores_df = db.querydatafromdatabase(sql, values, ['Score'])

        if scores_df.shape[0] > 0:
            fig = px.histogram(scores_df, x='Score', nbins=10, title='Player Scores Histogram')
            fig.update_layout(
                xaxis_title='Score',
                yaxis_title='Frequency',
                bargap=0.1
            )
            return fig
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
