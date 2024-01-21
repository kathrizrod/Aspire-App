from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.exceptions import PreventUpdate

from app import app

navlink_style = {
    'color': '#fff'
}

navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Aspire Football Academy", class_name="ms-2")),
                ],
                align="center",
                className = 'g-0'
            ),
            href="/home",
        ),
        dbc.NavLink("Home", href="/home", style=navlink_style),
        dbc.NavLink("Players", href="/players", style=navlink_style),
        dbc.NavLink("Coaches", href="/coaches", style=navlink_style),
        dbc.NavLink("Sessions", href="/sessions", style=navlink_style),
        dbc.NavLink("Payments", href="/payments", style=navlink_style),
        dbc.NavLink("Skills Test", href="/skillstest", style=navlink_style),
        dbc.NavLink("Log Out", href="/logout", style=navlink_style)
    ],
    dark=True,
    color='dark'
)