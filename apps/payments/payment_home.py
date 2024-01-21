from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash_mantine_components import DatePicker
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime, date
import dash_mantine_components as dmc
from app import app
from apps import dbconnect as db

@app.callback(
    [
        Output('paymentshome_paymentlist','children')
    ],
    [
        Input('url','pathname'),
        Input('package-dd','value'),
        Input('sdpicker','date'),
        Input('edpicker','date')
    ]
)
def paymentshome_paymentlist(pathname,filter_packagegroup,filter_startdate,filter_enddate):

    print("Filter End Date:", filter_enddate)

    if pathname == '/payments':
        sql = """SELECT transaction_id, CONCAT(player_firstname,' ',LEFT(player_middlename,1),'.',' ',player_lastname) AS player_name, package_name, payment_date, payment_amount
                 FROM transactions t
                 INNER JOIN packages g on t.package_id = g.package_id
                 INNER JOIN players y on t.player_id = y.player_id"""
        values = []
        cols = ['Transaction ID','Name', 'Package', 'Date', 'Amount']

    
        print("SQL Query:", sql, "Values:", values)

        if filter_packagegroup:
            if isinstance(filter_packagegroup, str):
                sql = "AND package_name ILIKE %s"
            filter_packagegroup_tuple = tuple(filter_packagegroup)
            if len(filter_packagegroup_tuple)==1:
                sql += " AND package_name ILIKE %s"
                values += [filter_packagegroup[0]]

            else:
                sql += f" AND package_name IN {filter_packagegroup_tuple}"


        if filter_startdate and filter_enddate:
            start_date = datetime.strptime(filter_startdate, '%Y-%m-%d')
            end_date = datetime.strptime(filter_enddate, '%Y-%m-%d')
            sql += " AND payment_date >= %s AND payment_date <= %s"
            values += [start_date, end_date]

        elif filter_startdate:
            start_date = datetime.strptime(filter_startdate, '%Y-%m-%d')
            sql += " AND payment_date >= %s"
            values += [start_date]


        elif filter_enddate:
            end_date = datetime.strptime(filter_enddate, '%Y-%m-%d')
            sql += " AND payment_date <= %s"
            values += [end_date]

        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:

            table = dbc.Table.from_dataframe(df, striped=True, bordered=False, hover=True, size='sm', className='center-table')
            table.style_cell = {
                'textAlign': 'center',
            }
            return [table]
        else:
            return[html.Div("No records to display")]
    else:
        raise PreventUpdate
    
@app.callback(
    [
        Output('paymentshome_salessummary','children')
    ],
    [
        Input('url','pathname'),
        Input('stdpicker','date'),
        Input('endpicker','date')
    ]
)

def paymentshome_salessummary(pathname, ft_startdate, ft_enddate):
     if pathname == '/payments':
        sql = """SELECT COALESCE(p.package_name, 'Total') AS "Package Type",
                COUNT(t.transaction_id) AS "Count",
                SUM(t.payment_amount) AS "Sum of payment_amount"
                FROM
                    packages p
                RIGHT JOIN
                    transactions t ON p.package_id = t.package_id"""
        values = []
        cols = ['Package Type','Count', 'Total Sales']

        
        date_filter_added = False
        if ft_startdate and ft_enddate:
            start_date = datetime.strptime(ft_startdate, '%Y-%m-%d')
            end_date = datetime.strptime(ft_enddate, '%Y-%m-%d')
            sql += " WHERE payment_date >= %s AND payment_date <= %s"
            values += [start_date, end_date]
            date_filter_added = True

        elif ft_startdate:
            start_date = datetime.strptime(ft_startdate, '%Y-%m-%d')
            sql += " WHERE payment_date >= %s"
            values += [start_date]
            date_filter_added = True

        elif ft_enddate:
            end_date = datetime.strptime(ft_enddate, '%Y-%m-%d')
            sql += " WHERE payment_date <= %s"
            values += [end_date]
            date_filter_added = True

        sql += """ GROUP BY
                    GROUPING SETS ((p.package_name), ())
                ORDER BY
                    CASE WHEN p.package_name IS NULL THEN 'Total' ELSE p.package_name END
	            """

        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            table = dbc.Table.from_dataframe(df, striped=False, bordered=False, hover=True, size='sm', className='center-table')
            table.style_cell = {
                'textAlign': 'center',
            }
            return [table]
        else:
            return [html.Div("No records to display")]
     else:
        raise PreventUpdate


layout = html.Div(
    [
        html.H2('Payments', style={'font-size': '24px'}),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                [
                                    html.H3('All Payments', style={'font-size': '20px'})
                                ]
                            ),
                            dbc.CardBody(
                                [
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Add Payment",
                                                href='/payments/payment_record',
                                                style={'font-size': '16px', 'margin-bottom': '10px'}
                                            )
                                        ]
                                    ),
                                    html.Hr(),
                                    html.Div(
                                        [
                                            html.H4('Filter Payments', style={'font-size': '18px'}),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            dbc.Label("Package", html_for='package-dd', style={'font-size': '16px'}),
                                                            dcc.Dropdown(
                                                                id='package-dd',
                                                                multi=True,
                                                                placeholder='Select Package',
                                                            )
                                                        ],
                                                        width=4
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dbc.Label("From", html_for='sdpicker', style={'display': 'block', 'font-size': '15px'}),
                                                            dcc.DatePickerSingle(
                                                                id='sdpicker',
                                                                placeholder='Select Date',
                                                                month_format='MMM Do, YY',
                                                            )
                                                        ],
                                                        width=2
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dbc.Label("To", html_for='edpicker', style={'display': 'block', 'font-size': '15px'}),
                                                            dcc.DatePickerSingle(
                                                                id='edpicker',
                                                                placeholder='Select Date',
                                                                month_format='MMM Do, YY',
                                                            )
                                                        ],
                                                        width=3
                                                    ),
                                                ],
                                                className='mb-3'
                                            ),
                                            html.Hr(),
                                            html.Div(
                                                "Table of payments goes here",
                                                id='paymentshome_paymentlist'
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    width=8  
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(
                                [
                                    html.H3('Sales Summary', style={'font-size': '20px'})
                                ]
                            ),
                            dbc.CardBody(
                                [
                                    html.Div(
                                        [
                                            html.H4('Filter Sales', style={'font-size': '18px'}),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            dbc.Label("From", html_for='stdpicker', style={'display': 'block', 'font-size': '15px'}),
                                                            dcc.DatePickerSingle(
                                                                id='stdpicker',
                                                                placeholder='Select Date',
                                                                month_format='MMM Do, YY',
                                                            )
                                                        ],
                                                        width=3
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dbc.Label("To", html_for='endpicker', style={'display': 'block', 'font-size': '15px'}),
                                                            dcc.DatePickerSingle(
                                                                id='endpicker',
                                                                placeholder='Select Date',
                                                                month_format='MMM Do, YY',
                                                            )
                                                        ],
                                                        width=3
                                                    ),
                                                ],
                                                className='mb-3'
                                            ),
                                            html.Hr(),
                                            html.Div(
                                                "Summary of monthly transactions will go here.",
                                                id='paymentshome_salessummary'
                                            ),
                                            html.Div(
                                                [
                                                    dbc.Button(
                                                        "View Sales Dashboard",
                                                        href='/payments/salesdb',
                                                        color="primary",
                                                        className="mr-1 btn-sm",
                                                        style={'text-decoration': 'none', 'font-size': '14px'}
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    ),
                    width=4 
                ),
            ]
        )
    ]
)

# package
@app.callback(
    [
        Output('package-dd', 'options')
    ],
    [
        Input('url', 'pathname')
    ]
)
def paymentrecord_populatepackage(pathname):
    if pathname == '/payments':
        sql = """
        SELECT package_name AS label, package_name As value
        FROM Packages
        """
        value = []
        cols = ['label', 'value']

        df = db.querydatafromdatabase(sql, value, cols)

        package_options = df.to_dict('records')
        return [package_options]

    else:
        raise PreventUpdate
    
# program
@app.callback(
    [
        Output('program-dd', 'options')
    ],
    [
        Input('url', 'pathname')
    ]
)
def paymentrecord_populateprogram(pathname):
    if pathname == '/payments/payments_home':
        sql = """
        SELECT program_name AS label, program_id As value
        FROM FbPrograms
        """
        value = []
        cols = ['label', 'value']

        df = db.querydatafromdatabase(sql, value, cols)

        program_options = df.to_dict('records')
        return [program_options]

    else:
        raise PreventUpdate

