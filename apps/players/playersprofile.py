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
        Output('playersprofile_info','children')
    ],
    [
        Input('url','pathname')
    ],
    [
        State('url','search')
    ]
)
def playersprofile_loadplayerinfo(pathname, search):
    if pathname == '/players/playersprofile':
        sql="""SELECT player_lastname, player_firstname, player_middlename, program_name, group_name 
        FROM players p
        INNER JOIN fbprograms f ON p.program_id = f.program_id
        INNER JOIN agegroups a ON p.group_id = a.group_id
        WHERE player_id = %s"""
    
        parsed=urlparse(search)
        playerid = parse_qs(parsed.query)['id'][0]
        values = [playerid]
        col = ['Last Name', 'First Name','Middle Name', 'Football Program','Age Group']

        df = db.querydatafromdatabase(sql,values,col)
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
        return[table]
    else:
        raise PreventUpdate
    
@app.callback(
    [
        Output('playersprofile_basicinfo','children')
    ],
    [
        Input('url','pathname')
    ],
    [
        State('url','search')
    ]
)
def playersprofile_loadbasicinfo(pathname, search):
    if pathname == '/players/playersprofile':
        sql="""SELECT player_birthday, date_part('year',age(player_birthday)) AS age, player_gender
        FROM players p
        WHERE player_id = %s"""
    
        parsed=urlparse(search)
        playerid = parse_qs(parsed.query)['id'][0]
        values = [playerid]
        col = ['Birthday', 'Age','Gender']

        df = db.querydatafromdatabase(sql,values,col)
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
        return[table]
    else:
        raise PreventUpdate
    
@app.callback(
    [
        Output('playersprofile_parentinfo','children')
    ],
    [
        Input('url','pathname')
    ],
    [
        State('url','search')
    ]
)
def playersprofile_loadbasicinfo(pathname, search):
    if pathname == '/players/playersprofile':
        sql="""SELECT pa.parent_lastname, pa.parent_firstname, pa.parent_middlename, pa.parent_contact
        FROM parents pa
        INNER JOIN players p ON p.parent_id = pa.parent_id
        WHERE player_id = %s"""
    
        parsed=urlparse(search)
        playerid = parse_qs(parsed.query)['id'][0]
        values = [playerid]
        col = ['Last Name', 'First Name','Middle Name', 'Contact Details']

        df = db.querydatafromdatabase(sql,values,col)
        table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
        return[table]
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('playersprofile_attendance','children')
    ],
    [
        Input('url','pathname')
    ],
    [
        State('url','search')
    ]
)
def playersprofile_loadattendance(pathname, search):
    if pathname == '/players/playersprofile':
        sql="""SELECT TO_CHAR(ts.session_date,'Mon DD, YYYY'), sch.schedule_time, sch.schedule_dotw
        FROM playerattendance pla
        JOIN trainingsession ts ON pla.session_id = ts.session_id
        JOIN transactions t ON pla.transaction_id = t.transaction_id
        JOIN players p ON t.player_id = p.player_id
        JOIN status s ON t.status_id = s.status_id
        JOIN schedules sch ON ts.schedule_id = sch.schedule_id
        WHERE p.player_id = %s 
        ORDER BY ts.session_date DESC"""

        parsed=urlparse(search)
        playerid = parse_qs(parsed.query)['id'][0]
        values = [playerid]
        col = ['Date','Time','Day']

        df = db.querydatafromdatabase(sql,values,col)

        total_sessions = df.shape[0]
        total_sessions_html = html.Div(
            dbc.Table.from_dataframe(pd.DataFrame({'Total:':[f'{total_sessions} Session/s Attended']}),size='sm'),
            style={'text-align':'right'}
        )

        table = [
            html.Div(
                dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm'),
                style={'max-height':'200px','overflowY':'scroll'}
            ),
            total_sessions_html
        ]
        return[table]
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('playersprofile_package', 'children'),
        Output('package_status', 'children')
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('url', 'search')
    ]
)
def playersprofile_loadpackage(pathname, search):
    if pathname == '/players/playersprofile':
        sql ="""SELECT TO_CHAR(T.payment_date,'Mon DD, YYYY'), PKG.package_name AS package_availed, (PKG.package_numsess - COUNT(PA.session_id)) AS remaining_sessions, s.status_name as status_name
        FROM transactions T
        JOIN packages PKG ON T.package_id = PKG.package_id
        LEFT JOIN playerattendance PA ON T.transaction_id = PA.transaction_id
        JOIN status s on t.status_id = s.status_id
        WHERE T.player_id = %s
        GROUP BY T.transaction_id, PKG.package_name, T.payment_date, PKG.package_numsess, s.status_name
        ORDER BY T.payment_date DESC
        LIMIT 1"""

        parsed = urlparse(search)
        playerid = parse_qs(parsed.query)['id'][0]
        values = [playerid]
        col = ['Payment Date','Package Availed', 'Remaining Sessions', 'Status']

        df = db.querydatafromdatabase(sql, values, col)

       
        remaining_sessions = int(df['Remaining Sessions'].iloc[0])
        status = df['Status'].iloc[0]

      
        if remaining_sessions == 0 and status == 'Active':
            update_status_sql = """UPDATE transactions
                                   SET status_id = (SELECT status_id FROM status WHERE status_name = 'Inactive')
                                   WHERE player_id = %s"""
            db.modifydatabase(update_status_sql, [playerid])

            
            updated_status_sql = """SELECT S.STATUS_NAME AS STATUS_NAME
                                    FROM TRANSACTIONS T
                                    JOIN STATUS S ON T.STATUS_ID = S.STATUS_ID
                                    WHERE T.PLAYER_ID = %s"""
            updated_status = db.querydatafromdatabase(updated_status_sql, [playerid], ['Status'])
            status = updated_status['Status'].iloc[0]

        table = html.Div(
            dbc.Table.from_dataframe(df[['Package Availed', 'Remaining Sessions', 'Payment Date']].head(10),
                                      striped=True, bordered=True, hover=True, size='sm')
        )

        status_indicator = html.Div([
            html.Span("Status: ", style={'color': 'black'}),
            html.Span(status, style={'color': 'green' if status == 'Active' else 'red'})
            ])


        return table, status_indicator
    else:
        raise PreventUpdate

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H2('Players Profile'),
                    width=8
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button(
                                        "Back",
                                        href='/players',
                                        id='playersprofile_back',
                                        color='secondary',
                                        className='mr-2',  
                                    ),
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        "Delete",
                                        id='player_delete',
                                        color='danger',
                                        n_clicks=0,
                                    ),
                                ),
                            ],
                            className="justify-content-end",  
                        ),
                    ],
                    width=4,
                    style={'text-align': 'right'}
                ),
            ],
            className="mb-4",
            style={'marginRight': '0', 'marginLeft': '0'}
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader('Basic Information', style={'font-weight': '600', 'font-size': '20px'}),
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    "Table with player info will go here.",
                                                    id='playersprofile_info'
                                                ),
                                                html.Div(
                                                    "Table with bday and gender goes here",
                                                    id='playersprofile_basicinfo'
                                                )
                                            ]
                                        ),
                                    ]
                                )
                            ]
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader('Parent/Guardian Information', style={'font-weight': '600', 'font-size': '20px'}),
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            [
                                                html.Div(
                                                    "Table with player info will go here.",
                                                    id='playersprofile_parentinfo'
                                                ),
                                            ]
                                        ),
                                    ]
                                )
                            ]
                        ),
                    ]
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader('Sessions Attended',style={'font-weight': '600', 'font-size': '20px'}),
                            dbc.CardBody(
                                [
                                    html.Div(
                                        [
                                            html.Div(
                                                "Table with attendance will go here",
                                                id='playersprofile_attendance'
                                            )
                                        ],
                                    )
                                ]
                            )
                        ]
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader('Package Availed', id='package_status', style={'font-weight': '600', 'font-size': '20px'}),
                            dbc.CardBody(
                                html.Div(
                                    [
                                        html.Div(
                                            "Table with package and status will go here",
                                            id = 'playersprofile_package'
                                        ),
                                    ]
                                )
                            )
                        ]
                    )
                )
            ], style={'marginBottom': 20, 'marginTop': 20}
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Performance Chart",style={'font-weight': '600', 'font-size': '20px'}),
                            dbc.CardBody(
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id='playersprofile_performancechart'
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader('Skills Tests Scores',style={'font-weight': '600', 'font-size': '20px'}),
                            dbc.CardBody(
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dcc.Dropdown(
                                                        id='playersprofile_skillstestfilter',
                                                        placeholder='Choose Skill Test',
                                                        multi=True
                                                    ), 
                                                    width = 5,
                                                    style={'marginBottom': 20}
                                                ),
                                                dbc.Col(
                                                    dbc.Button(
                                                        'Clear',
                                                        id = 'playersprofile_filterreset',
                                                        color='secondary',
                                                        n_clicks=0
                                                    ),
                                                    width = 3,
                                                    style={'marginBottom':20}
                                                ),
                                            ]
                                        ), 
                                        html.Div(
                                            "Table with skills tests scores goes here",
                                            id='playersprofile_skillstestscores'
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                )
            ]
        ),
        dbc.Modal(
            [
                dbc.ModalHeader(html.H4('Delete Player')),
                dbc.ModalBody("Are you sure you want to delete this player?", style={'text-align': 'center'}),
                dbc.ModalFooter(
                    [
                        dbc.Button("Proceed", id='player_godelete', n_clicks=0),
                        dbc.Button("No", href="/players")
                    ]
                )
            ],
            centered=True,
            id="playerdelete_successmodal",
            backdrop='static'
        )
    ]
)

@app.callback(
    [Output('playerdelete_successmodal', 'is_open')],
    [Input('player_delete', 'n_clicks')]
)
def player_delete(deletebtn):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'player_delete' and deletebtn:
            return [True]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate


@app.callback(
    [Output('player_godelete', 'href')],
    [Input('player_godelete', 'n_clicks')],
    [Input('url', 'search')]
)
def skillstest_delete(deletebtn, search):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'player_godelete' and deletebtn:
            sql = """ UPDATE players
                SET player_isdeleted = %s
                WHERE players.player_id = %s
            """

            parsed = urlparse(search)
            playerid = parse_qs(parsed.query)['id'][0]
            values = [True, playerid]

            db.modifydatabase(sql, values)

            return_href = "/players"
            return [return_href]
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('playersprofile_performancechart','figure'),
        Output('playersprofile_skillstestscores','children')
    ],
    [
        Input('url','pathname'),
        Input('playersprofile_skillstestfilter','value')
    ],
    [
        State('url','search')
    ]
)
def playersprofile_loadskillstestscores(pathname, filter_skillstest, search):
    if pathname == '/players/playersprofile':
        sql="""SELECT PS.test_date, ST.skill_name, PS.score_skill, ST.skill_scoreunit
        FROM PlayerScore PS
        JOIN players P ON P.player_id = PS.player_id
        JOIN SkillsTest ST ON PS.skill_id = ST.skill_id
        WHERE PS.player_id = %s"""

        parsed = urlparse(search)
        playerid = parse_qs(parsed.query)['id'][0]
        values = [playerid]
        col = ['test_date','skill_name','score_skill', 'Unit of Measurement']

        if filter_skillstest:
            if isinstance(filter_skillstest, str):
                filter_skillstest=[filter_skillstest]
            filter_skillstest_tuple = tuple(filter_skillstest)
            if len(filter_skillstest_tuple)==1:
                sql += " AND ST.skill_name ILIKE %s"
                values += [filter_skillstest_tuple[0]]
            else:
                sql += f" AND ST.skill_name IN {filter_skillstest_tuple}"

        df = db.querydatafromdatabase(sql,values,col)
        df = df.rename(columns={'test_date':'Date','skill_name':'Skill Test','score_skill':'Score'})
        
        df = df.sort_values(by='Date')
        
        chart_fig = px.line(df, x='Date',y='Score', color='Skill Test',
                            labels={'Date':'Date', 'Score':'Score', 'Skill Test':'Skill Test'},
                            title='Scores per Skill Test Over Time',
                            markers=True, line_shape='linear')

        table_div = html.Div(
            dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm'),
            style={'max-height':'200px','overflowY':'scroll'}
            )

        return chart_fig, table_div
    else:
        raise PreventUpdate

@app.callback(
    [
        Output('playersprofile_skillstestfilter','options')
    ],
    [
        Input('url','pathname')
    ]
)
def playersprofile_populateskillstest(pathname):
    if pathname == '/players/playersprofile':
        sql = """
        SELECT skill_name as label, skill_name as value
        FROM SkillsTest
        """
        values = []
        cols = ['label','value']

        df = db.querydatafromdatabase(sql, values, cols)
        
        skillstest_options = df.to_dict('records')
        return [skillstest_options]
    else:
        raise PreventUpdate
    
@app.callback(
    [
        Output('playersprofile_skillstestfilter','value')
    ],
    [
        Input('playersprofile_filterreset','n_clicks')
    ]
)
def playersprofile_resetfilters(n_clicks):
    if n_clicks>0:
        return [None]
    else:
        return dash.no_update