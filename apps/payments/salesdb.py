from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash
from dash.exceptions import PreventUpdate
import pandas as pd
from datetime import datetime, date, timedelta

import dash_mantine_components as dmc
import plotly.graph_objects as go
import plotly.express as px

from app import app
from apps import dbconnect as db


# total counts KS
@app.callback(
    [
        Output('sldb_totalcountks', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('sdp', 'date'),  
        Input('edp', 'date'),  
    ]
)
def salesdashboard_tcks(pathname, filter_startdate, filter_enddate):
    if pathname == '/payments/salesdb':
        if filter_startdate is None or filter_enddate is None:
           
            filter_startdate = datetime(datetime.now().year, 1, 1).strftime('%Y-%m-%d')
            filter_enddate = datetime(datetime.now().year, 12, 31).strftime('%Y-%m-%d')
        sql = """ SELECT
                    COUNT(*) AS total_transactions
                FROM
                    transactions t
                JOIN
                    Packages p ON t.package_id = p.package_id
                WHERE
                    p.program_id = 1
                    AND (t.payment_date BETWEEN %s AND %s);"""  

        values = [filter_startdate, filter_enddate]
        col = ['']

        df = db.querydatafromdatabase(sql, values, col)

       
        total_count = df.iloc[0, 0]

        
        count_element = html.Div(f"{total_count}")

        return [count_element]

    else:
        raise PreventUpdate

# sld_totalsalesks
@app.callback(
    [
        Output('sldb_totalsalesks', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('sdp', 'date'),  
        Input('edp', 'date'), 
    ]
)
def salesdashboard_tsks(pathname, filter_startdate, filter_enddate):
    if pathname == '/payments/salesdb':
        if filter_startdate is None or filter_enddate is None:
            
            filter_startdate = datetime(datetime.now().year, 1, 1).strftime('%Y-%m-%d')
            filter_enddate = datetime(datetime.now().year, 12, 31).strftime('%Y-%m-%d')
        sql = """ SELECT
                    SUM(t.payment_amount) AS total_sales
                FROM
                    transactions t
                JOIN
                    Packages p ON t.package_id = p.package_id
                WHERE
                    p.program_id = 1
                    AND (t.payment_date BETWEEN %s AND %s);"""  

        values = [filter_startdate, filter_enddate]
        col = ['']

        df = db.querydatafromdatabase(sql, values, col)

        
        total_sales = df.iloc[0, 0]

       
        sales_element = html.Div(f"{total_sales}")

        return [sales_element]

    else:
        raise PreventUpdate

# total count EL
@app.callback(
    [
        Output('sldb_totalcountel', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('sdp', 'date'),  
        Input('edp', 'date'),  
    ]
)
def salesdashboard_tcel(pathname, filter_startdate, filter_enddate):
    if pathname == '/payments/salesdb':
        if filter_startdate is None or filter_enddate is None:
           
            filter_startdate = datetime(datetime.now().year, 1, 1).strftime('%Y-%m-%d')
            filter_enddate = datetime(datetime.now().year, 12, 31).strftime('%Y-%m-%d')

        sql = """ SELECT
                    COUNT(*) AS total_transactions
                FROM
                    transactions t
                JOIN
                    Packages p ON t.package_id = p.package_id
                WHERE
                    p.program_id = 2
                    AND (t.payment_date BETWEEN %s AND %s);"""  

        values = [filter_startdate, filter_enddate]
        col = ['']

        df = db.querydatafromdatabase(sql, values, col)

        
        total_count = df.iloc[0, 0]

        
        count_element = html.Div(f"{total_count}")

        return [count_element]

    else:
        raise PreventUpdate

# sld_totalsalesel
@app.callback(
    [
        Output('sldb_totalsalesel', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('sdp', 'date'),  
        Input('edp', 'date'),  
    ]
)
def salesdashboard_tsel(pathname, filter_startdate, filter_enddate):
    if pathname == '/payments/salesdb':
        if filter_startdate is None or filter_enddate is None:
           
            filter_startdate = datetime(datetime.now().year, 1, 1).strftime('%Y-%m-%d')
            filter_enddate = datetime(datetime.now().year, 12, 31).strftime('%Y-%m-%d')

        sql = """ SELECT
                    SUM(t.payment_amount) AS total_sales
                FROM
                    transactions t
                JOIN
                    Packages p ON t.package_id = p.package_id
                WHERE
                    p.program_id = 2
                    AND (t.payment_date BETWEEN %s AND %s);"""  

        values = [filter_startdate, filter_enddate]
        col = ['']

        df = db.querydatafromdatabase(sql, values, col)

        
        total_sales = df.iloc[0, 0]

       
        sales_element = html.Div(f"{total_sales}")

        return [sales_element]

    else:
        raise PreventUpdate

#Program Sales Share
@app.callback(
    [
        Output('sld_pie', 'figure'),
        Output('sld_piet', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('sdp','date'),
        Input('edp','date'),
    ]
)
def salesdashboard_programshare(pathname, filter_startdate, filter_enddate):
    if pathname == '/payments/salesdb':
      
        if not filter_startdate:
            filter_startdate = datetime(datetime.now().year, 1, 1).date()
        if not filter_enddate:
            filter_enddate = datetime(datetime.now().year, 12, 31).date()

        sql = """ SELECT
                    CASE
                        WHEN p.program_id = 1 THEN 'Kickstart'
                        WHEN p.program_id = 2 THEN 'Elite'
                        ELSE 'Other'
                    END AS program_type,
                    SUM(t.payment_amount) AS total_sales
                FROM
                    transactions t
                JOIN
                    Packages p ON t.package_id = p.package_id
                WHERE
                    p.program_id IN (1, 2)
                    AND t.payment_date BETWEEN %s AND %s
                GROUP BY
                    program_type"""

        values = [filter_startdate, filter_enddate]
        col = ['program_type','total_sales']

        df = db.querydatafromdatabase(sql, values, col)

   
        chart_fig = px.pie(
            df,
            names='program_type',
            values='total_sales',
            labels={'total_sales': 'Total Sales', 'program_type': 'Program Type'},
            hole=0.3
        )

    
        table_div = html.Div(
            dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm'),
            style={'max-height':'200px','overflowY':'scroll'}
            
        )

        return chart_fig, table_div

    else:
        raise PreventUpdate


# Monthly
@app.callback(
    [
        Output('sld_line', 'figure'),
        Output('sld_linet', 'children'),
    ],
    [
        Input('url', 'pathname'),
        Input('year-dropdown', 'value'), 
    ]
)
def salesdashboard_monthlyshares(pathname, selected_year):
    if pathname == '/payments/salesdb' and selected_year is not None:
        sql = """SELECT
                    CASE
                        WHEN p.program_id = 1 THEN 'Kickstart'
                        WHEN p.program_id = 2 THEN 'Elite'
                        ELSE 'Other'
                    END AS program_type,
                    EXTRACT(MONTH FROM t.payment_date) AS month_number,
                    SUM(t.payment_amount) AS total_sales
                FROM
                    transactions t
                JOIN
                    Packages p ON t.package_id = p.package_id
                WHERE
                    p.program_id IN (1, 2)
                    AND EXTRACT(YEAR FROM t.payment_date) = %s
                GROUP BY
                    program_type, month_number
                ORDER BY
                    program_type, month_number;"""

        values = [selected_year]
        col = ['program_type', 'month_number', 'total_sales']

        df = db.querydatafromdatabase(sql, values, col)

    
        chart_fig = px.line(
            df, x='month_number', y='total_sales', color='program_type',
            labels={'month_number': 'Month', 'total_sales': 'Total Sales'},
            title='Monthly Sales'
        )

      
        table_div = html.Div(
            dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm'),
            style={'max-height': '200px', 'overflowY': 'scroll'}
        )

        return chart_fig, table_div

    else:
        raise PreventUpdate


#Package Sales Share
@app.callback(
    [
        Output('sld_bar', 'figure'),
        Output('sld_bart', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('sdp','date'),
        Input('edp','date'),
    ]
)
def salesdashboard_packageshare(pathname, filter_startdate, filter_enddate):
    if pathname == '/payments/salesdb':
   
        if not filter_startdate:
            filter_startdate = datetime(datetime.now().year, 1, 1).date()
        if not filter_enddate:
            filter_enddate = datetime(datetime.now().year, 12, 31).date()

        sql = """ SELECT
                        p.package_name,
                        SUM(t.payment_amount) AS total_sales
                    FROM
                        transactions t
                    JOIN
                        Packages p ON t.package_id = p.package_id
                    JOIN
                        FbPrograms fp ON p.program_id = fp.program_id
                    WHERE
                        t.payment_date BETWEEN %s AND %s
                    GROUP BY
                        p.package_name
                    ORDER BY
                        total_sales ASC;"""

        values = [filter_startdate, filter_enddate]
        col = ['package_name','total_sales']

        df = db.querydatafromdatabase(sql, values, col)


        chart_fig = px.bar(
            df,
            x='package_name',
            y='total_sales',
            labels={'total_sales': 'Total Sales', 'program_type': 'Program Type'},
        )

   
        table_div = html.Div(
            dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm'),
            style={'max-height':'200px','overflowY':'scroll'}
            
        )

        return chart_fig, table_div

    else:
        raise PreventUpdate


layout = html.Div(style={'textAlign': 'center'}, children=[
 
    html.H1("Aspire Academy", style={'margin': '30px'}),

  
    dbc.Row([
       
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.Div(
                        [
                            html.H4('Filter', style={'font-size': '18px'}),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Label("From", html_for='sdp', style={'display': 'block', 'font-size': '15px'}),
                                            dcc.DatePickerSingle(
                                                id='sdp',
                                                placeholder='Select Date',
                                                month_format='MMM Do, YY',
                                            )
                                        ],
                                        width=5
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Label("To", html_for='edp', style={'display': 'block', 'font-size': '15px'}),
                                            dcc.DatePickerSingle(
                                                id='edp',
                                                placeholder='Select Date',
                                                month_format='MMM Do, YY',
                                            )
                                        ],
                                        width=5
                                    ),
                                ],
                                className='mb-3',
                                justify='center',
                                align='center',
                            ),
                        ]
                    )
                ])
            ]),
            width=4
        ),
     
        dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H3("Kickstart")),
                dbc.CardBody([
                    html.Div([
                        dbc.Row([
                            # Total Count
                            dbc.Col(
                                [
                                    html.Div("Total Count", style={'font-size': '18px'}),
                                    html.Div(
                                        id='sldb_totalcountks'
                                    ),
                                ],
                                width=6
                            ),
                            # Total Sales
                            dbc.Col(
                                [
                                    html.Div("Total Sales", style={'font-size': '18px'}),
                                    html.Div(
                                        id='sldb_totalsalesks'
                                    ),
                                ],
                                width=6
                            ),
                        ]),
                    ])
                ])
            ]),
            width=4
     
        ),
       dbc.Col(
            dbc.Card([
                dbc.CardHeader(html.H3("Elite")),
                dbc.CardBody([
                    html.Div([
                        dbc.Row([
                            # Total Count
                            dbc.Col(
                                [
                                    html.Div("Total Count", style={'font-size': '18px'}),
                                    html.Div(
                                        id='sldb_totalcountel'
                                    ),
                                ],
                                width=6
                            ),
                            # Total Sales
                            dbc.Col(
                                [
                                    html.Div("Total Sales", style={'font-size': '18px'}),
                                    html.Div(
                                        id='sldb_totalsalesel'
                                    ),
                                ],
                                width=6
                            ),
                        ]),
                    ])
                ])
            ]),
            width=4
       )  
    ]),

   
    html.Hr(),
    dbc.Row([
       
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H5('Program Sales Share'),
                    dcc.Graph(
                        id='sld_pie',
                        
                    ),
                    html.Div(
                        "Table with Sales Shareds goes here",
                        id='sld_piet'
                    ),
                ])
            ]),
            width=4
        ),
     
        dbc.Col(
        dbc.Card([
            dbc.CardBody([
                html.H5('Monthly Sales'),

             
                html.Div([
                    dbc.Label("Select Year", html_for='year-dropdown', style={'display': 'block', 'font-size': '15px'}),
                    dcc.Dropdown(
                        id='year-dropdown',
                        options=[
                            {'label': str(year), 'value': year} for year in range(datetime.now().year, datetime.now().year - 5, -1)
                        ],
                        value=datetime.now().year,
                    ),
                ], style={'margin-top': '10px'}),

                dcc.Graph(
                    id='sld_line',
                ),
                html.Div(
                    "Table with Monthly sales goes here",
                    id='sld_linet'
                ),
            ])
        ]),
        width=4
    ),
     
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                     html.H5('Package Sales Share'),
                    dcc.Graph(
                        id='sld_bar',
                    ),
                    html.Div(
                        "Table with package sales goes here",
                        id='sld_bart'
                    ),
                ])
            ]),
            width=4
        ),
    ])
])
