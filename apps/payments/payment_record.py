from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash
from dash.exceptions import PreventUpdate
import pandas as pd
from datetime import datetime, date

import dash_mantine_components as dmc
from dash import Input, Output, html, callback

from psycopg2.extras import Json
from app import app
from apps import dbconnect as db

@app.callback(
    Output('payment-amount', 'value'),
    [
        Input('package-dropdown', 'value'),
        Input('url', 'pathname')
    ]
)
def paymentrecord_populateamount(selected_package_id, pathname):
    if pathname == '/payments/payment_record' and selected_package_id:
        sql = """
        SELECT package_price as price
        FROM Packages
        WHERE package_id = %s
        """
        value = [selected_package_id]
        cols = ['Price']

        df = db.querydatafromdatabase(sql, value, cols)
        price = df['Price'].iloc[0]

        return price
    else:
        raise PreventUpdate


layout = html.Div(
    [
        html.H2('Payment Details'),
        html.Hr(),
        dbc.Alert(id='paymentrecord_alert', is_open=False),
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("Player Name", html_for='player-dropdown', style={'display': 'block', 'font-size': '15px'}),
                                dcc.Dropdown(
                                    id='player-dropdown',
                                    placeholder="Select Player",
                                ),
                            ],
                            width=8  
                        ),
                        dbc.Col(
                            [
                                dbc.Button('+ Add New Player', href = '/players/playersadd',style={'margin-top': '31px'}),  
                            ],
                            width=4  
                        ),
                    ],
                    className='mb-3'
                ),

                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("Package", html_for='package-dropdown', style={'display': 'block', 'font-size': '15px'}),
                                dcc.Dropdown(
                                    id='package-dropdown',
                                    placeholder="Select Package",
                                ),
                            ],
                            width=5
                        ),
                        dbc.Col(
                            [
                                dbc.Label("Payment Amount", html_for='payment-amount', style={'display': 'block', 'font-size': '15px'}),
                                dcc.Input(
                                    id='payment-amount',
                                    type='number',
                                    style={'border': '1px solid #ced4da',
                                        'padding': '0.5em',
                                        'font-size': '14px',
                                        'font-family': 'inherit',
                                        'height': '35px',
                                        'border-radius': '5px',
                                        'font-weight': 'normal',
                                        },
                                ),
                            ],
                            width=2
                        ),
                    ],
                    className='mb-3'        
                ),

                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    [   dbc.Label("Date of Payment", html_for='date-picker', style={'display': 'block', 'font-size': '15px'}),
                                        dcc.DatePickerSingle(
                                            id='date-picker',
                                            placeholder='Select Date',
                                            month_format='MMM Do, YY',
                                        )
                                    ]
                                ),
                            ],
                            width=1
                        ),
                        dbc.Col(
                            [
                                dbc.Label("Mode of Payment", html_for='payment mode', style={'display': 'block', 'font-size': '15px'}),
                                dcc.Dropdown(
                                    id='payment mode',
                                    options=[
                                        {'label': 'Cash', 'value': 'Cash'},
                                        {'label': 'GCash', 'value': 'GCash'},
                                        {'label': 'Maya', 'value': 'Maya'},
                                        {'label': 'Bank Transfer', 'value': 'Bank Transfer'},
                                        {'label': 'Cheque', 'value': 'Cheque'},
                                        {'label': 'Others', 'value': 'Others'},
                                    ],
                                    placeholder="Select Mode of Payment",
                                ),
                            ],
                            width=5
                        ),
                    ],
                    className='mb-3'
                ),

            ]
        ),
       
        
        
        dbc.Button(
            'Submit',
            id='paymentrecord_submit',
            n_clicks=0,
            
        ),

    

        dbc.Modal(
            [
                dbc.ModalBody(
                    'Payment Recorded Successfully!'
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Proceed",
                        href='/payments'
                    )
                )
            ],
            centered=True,
            id='paymentrecord_successmodal',
            backdrop='static'
        )
    ],
)

# player
@app.callback(
    [
        Output('player-dropdown', 'options')
    ],
    [
        Input('url', 'pathname')
    ]
)
def paymentrecord_populateplayers(pathname):
    if pathname == '/payments/payment_record':
        sql = """
        SELECT CONCAT(player_firstname,' ',LEFT(player_middlename,1),'.',' ',player_lastname) AS label, player_id as value
        FROM Players
        """
        value = []
        cols = ['label', 'value']

        df = db.querydatafromdatabase(sql, value, cols)

        player_options = df.to_dict('records')
        return [player_options]

    else:
        raise PreventUpdate


# package
@app.callback(
    [
        Output('package-dropdown', 'options')
    ],
    [
        Input('url', 'pathname')
    ]
)
def paymentrecord_populatepackage(pathname):
    if pathname == '/payments/payment_record':
        sql = """
        SELECT package_name AS label, package_id As value
        FROM Packages
        """
        value = []
        cols = ['label', 'value']

        df = db.querydatafromdatabase(sql, value, cols)

        package_options = df.to_dict('records')
        return [package_options]

    else:
        raise PreventUpdate
    
# Mode of payment
@app.callback(
    dash.dependencies.Output('selected-mode-output', 'children'),
    [dash.dependencies.Input('payment-mode', 'value')]
)
def update_output(selected_mode):
    return f'Selected Mode of Payment: {selected_mode}'

@app.callback(
    [
        Output('paymentrecord_alert', 'color'),
        Output('paymentrecord_alert', 'children'),
        Output('paymentrecord_alert', 'is_open'),
        Output('paymentrecord_successmodal', 'is_open')
    ],
    [
        Input('paymentrecord_submit', 'n_clicks')
    ],
    [
        State('player-dropdown', 'value'),
        State('package-dropdown', 'value'),
        State('date-picker', 'date'),
        State('payment-amount', 'value'),
        State('payment mode', 'value'),
    ]
)
def paymentrecord_saveprofile(n_clicks,Player, Package, PaymentDate, Amount, Mode):
    ctx = dash.callback_context
    if ctx.triggered_id == 'paymentrecord_submit' and n_clicks:

        alert_open = False
        modal_open = False
        alert_color = ''
        alert_text = ''

        if not Player:
            alert_open = True
            alert_color = 'danger'
            alert_text = '*Player field is required.'
        elif not Package:
            alert_open = True
            alert_color = 'danger'
            alert_text = '*Package field is required'
        elif not PaymentDate or (isinstance(PaymentDate, str) and not PaymentDate.strip()):
            alert_open = True
            alert_color = 'danger'
            alert_text = '*Date of Payment field is required.'
        elif not Amount:
            alert_open = True
            alert_color = 'danger'
            alert_text = '*Payment Amount field is required.'

        elif not Mode:
            alert_open = True
            alert_color = 'danger'
            alert_text = '*Payment Mode field is required.'
        else:
            sql = '''
                INSERT INTO transactions (payment_amount, payment_date, payment_mode, package_id,
                    player_id,status_id)
                VALUES (%s,%s,%s,%s,%s,%s)
            '''
            values = [Amount, PaymentDate, Mode, Package, Player,'1']

            db.modifydatabase(sql, values)
            modal_open = True

        return [alert_color, alert_text, alert_open, modal_open]
    else:
        raise PreventUpdate