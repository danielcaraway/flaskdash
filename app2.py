from flask import Flask
from flask import Flask, render_template, url_for
import dash
import dash_core_components as dcc
import dash_html_components as html

app = Flask(__name__)
dashapp = dash.Dash(__name__)

@app.route('/')
def index():
    # return "Hello, world!"
    # return render_template('index.html')
    return "
    dashapp.layout = html.Div([
        html.H2('PICK A CITY, ANY CITY!'),
        dcc.Dropdown(
            id='dropdown',
            options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
            value='LA'
        ),
        html.Div(id='display-value')
    ])

    @dashapp.callback(dash.dependencies.Output('display-value', 'children'),
                [dash.dependencies.Input('dropdown', 'value')])

    def display_value(value):
        return 'You have selected "{}"'.format(value)
        "


if __name__ == "__main__":
    app.run(debug=True)