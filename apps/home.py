import dash
from dash import html
import dash_bootstrap_components as dbc


layout = html.Div([
    # Main content area with dark blue background
    html.Div([
        # Header with bolder and bigger text
        html.H1("Welcome to Aspire Football Academy", className="display-4 text-white mb-4 font-weight-bolder",
                style={'color': 'white', 'font-size': '2.8em'}),
        html.H2("PH Training Management System", className="display-4 text-white mb-4 font-weight-bolder",
                style={'color': 'white', 'font-size': '2.8em'}),

        # Thick line separator with white color
        html.Hr(style={'border-top': 'thick double white'}),

        # Body text in white, bold, and a little bit smaller
        html.P("Player Management: Add, view, and update player information.", className="lead text-white font-weight-bold",
               style={'font-size': '1.5em', 'line-height': '1.4'}),
        html.P("Session Scheduler: Schedule and organize training sessions.", className="lead text-white font-weight-bold",
               style={'font-size': '1.5em', 'line-height': '1.4'}),
        html.P("Payment Processing: Handle player payments and financial transactions.", className="lead text-white font-weight-bold",
               style={'font-size': '1.5em', 'line-height': '1.4'}),
        html.P("Reports: Generate reports to track performance, attendance, and more.", className="lead text-white font-weight-bold",
               style={'font-size': '1.5em', 'line-height': '1.4'}),

        # Thick line separator with white color
        html.Hr(style={'border-top': 'thick double white'}),

        # Additional text in bolder and bigger, UI blue color
        html.P("Aspire Football Academy is a premier training institution dedicated to the "
               "development of young talents in football. Our state-of-the-art facilities and "
               "professional coaching staff ensure that players receive the best training experience.",
               className="text-white font-weight-bolder", style={'font-size': '1.7em', 'color': 'white'}),

        # Buttons column with UI orange buttons, left-aligned and centered text
        dbc.Col([
            dbc.Button("Player Profiles", color="primary", className="mb-3", href='/players',
                       style={'background-color': 'orange', 'width': '60%', 'text-align': 'center'}),
            dbc.Button("Sales Report", color="primary", className="mb-3", href='/payments/salesdb', style={'background-color': 'orange', 'width': '60%', 'text-align': 'center'}),
            dbc.Button("Skills Reports", color="primary", className="mb-3", href='/skillstest', style={'background-color': 'orange', 'width': '60%', 'text-align': 'center'}),
            dbc.Button("Attendance Report", color="primary", className="mb-3", href='/sessions', style={'background-color': 'orange', 'width': '60%', 'text-align': 'center'}),
        ], className="mt-4", width=2, align='start')
    ], style={'background-color': 'darkblue', 'width': '100%', 'height': '100vh', 'padding': '20px'}),
])