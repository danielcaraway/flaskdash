from flask import Flask
from flask import Flask, render_template, url_for
import dash
import dash_core_components as dcc
import dash_html_components as html

server = Flask(__name__)


@server.route('/')
def index():
    return 'Hello Flask app'

app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/dash/'
)

# app.layout = html.Div("My Dash app")

app.layout = html.Div([
    html.H2('PICK A CITY, ANY CITY!'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value')
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
            [dash.dependencies.Input('dropdown', 'value')])

def display_value(value):
    return 'You have selected "{}"'.format(value)
    
if __name__ == '__main__':
    app.run_server(debug=True)  