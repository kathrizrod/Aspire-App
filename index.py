from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import webbrowser

from app import app
from apps import commonmodules as cm
from apps import home
from apps.skillstest import skillstesthome, skillstestprofile, skillstestdetails, skillstestaddscore, deleteplayerscore
from apps.coaches import coacheshome, addcoach, deletecoach
from apps.players import playershome, playersadd, playersprofile
from apps.login import login as lg
from apps.login import signup as su
from apps.sessions import sessions, sessionsadd, attendanceadd, attendanceview
from apps.payments import payment_home, payment_record, salesdb

CONTENT_STYLE = {
    'margin-top': "4em",
    "margin-left": "1em",
    "margin-right": "1em",
    "padding": "1em 1em",
}

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=True),

        dcc.Store(id='sessionlogout', data=True, storage_type='session'),

        dcc.Store(id='currentuserid', data=-1, storage_type='session'),
        dcc.Store(id='currentrole', data=-1, storage_type='session'),

        html.Div(
            cm.navbar,
            id='navbar_div'
        ),

        html.Div(id='page-content', style=CONTENT_STYLE),
    ]
)

@app.callback(
    [
        Output('page-content', 'children'),
        Output('sessionlogout', 'data'),
        Output('navbar_div', 'className'),
    ],
    [
        Input('url', 'pathname')
    ],
    [
        State('sessionlogout', 'data'),
        State('currentuserid', 'data')
    ]
)
def displaypage (pathname, sessionlogout, userid):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
        if eventid == 'url':
            if userid < 0:
                if pathname == '/':
                    returnlayout = lg.layout
                elif pathname == '/signup':
                    returnlayout = su.layout
                else:
                    returnlayout = '404: request not found'
            else:
                if pathname == '/logout':
                    returnlayout = lg.layout
                    sessionlogout = True
                elif pathname == '/' or pathname == '/home':
                    returnlayout = home.layout
                elif pathname == '/skillstest':
                    returnlayout = skillstesthome.layout
                elif pathname == '/skillstest/skillstestprofile':
                    returnlayout = skillstestprofile.layout
                elif pathname == '/skillstest/skillstestdetails':
                    returnlayout = skillstestdetails.layout
                elif pathname == '/skillstest/skillstestaddscore':
                    returnlayout = skillstestaddscore.layout
                elif pathname == '/skillstest/deleteplayerscore':
                    returnlayout = deleteplayerscore.layout
                elif pathname == '/coaches':
                    returnlayout = coacheshome.layout
                elif pathname == '/coaches/addcoach':
                    returnlayout = addcoach.layout
                elif pathname == '/coaches/deletecoach':
                    returnlayout = deletecoach.layout
                elif pathname == '/players':
                    returnlayout = playershome.layout
                elif pathname == '/players/playersadd':
                    returnlayout = playersadd.layout
                elif pathname == '/players/playersprofile':
                    returnlayout = playersprofile.layout
                elif pathname == '/sessions':
                    returnlayout = sessions.layout
                elif pathname == '/sessions/sessionsadd':
                    returnlayout = sessionsadd.layout
                elif pathname == '/sessions/attendanceview':
                    returnlayout = attendanceview.layout
                elif pathname == '/sessions/attendanceadd':
                    returnlayout = attendanceadd.layout
                elif pathname == '/payments':
                    returnlayout = payment_home.layout
                elif pathname == '/payments/payment_record':
                    returnlayout = payment_record.layout
                elif pathname == '/payments/salesdb':
                    returnlayout = salesdb.layout
                else:
                    returnlayout = "error404"
            
            logout_conditions = [
                pathname in ['/', '/logout'],
                userid == -1,
                not userid
            ]
            sessionlogout = any(logout_conditions)
            
            # hide navbar if logged-out; else, set class/style to default
            navbar_classname = 'd-none' if sessionlogout else ''

        
        else:
            raise PreventUpdate
        
        return [returnlayout, sessionlogout, navbar_classname]

    else:
        raise PreventUpdate

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=False)