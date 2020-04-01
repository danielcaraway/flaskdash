from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                   dtype={"fips": str})

import plotly.express as px

fig = px.choropleth(df, geojson=counties, locations='fips', color='unemp',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           scope="usa",
                           labels={'unemp':'unemployment rate'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

import requests
from bs4 import BeautifulSoup as bs
url = "https://www.worldometers.info/coronavirus/"
page = requests.get(url)
soup= bs(page.content, "html.parser")

content_block = soup.find(id="main_table_countries_today")
# content_block

def tableDataText(table):       
    rows = []
    trs = table.find_all('tr')
    headerow = [td.get_text(strip=True) for td in trs[0].find_all('th')] # header row
    if headerow: # if there is a header row include first
        rows.append(headerow)
        trs = trs[1:]
    for tr in trs: # for every table row
        rows.append([td.get_text(strip=True) for td in tr.find_all('td')]) # data row
    return rows

list_table = tableDataText(content_block)
dftable = pd.DataFrame(list_table[1:], columns=list_table[0])



from flask import Flask, render_template, url_for
import dash
import dash_core_components as dcc
import dash_html_components as html


server = Flask(__name__)


@server.route('/')
def index():
    return 'Hello Flask app ' + dftable.columns[0]

app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/dash/'
)

# app.layout = html.Div("My Dash app")

app.layout = html.Div([
    html.H2('PICK A CITY, ANY CITY!?'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value'),
    dcc.Graph(figure=fig)
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
            [dash.dependencies.Input('dropdown', 'value')])

def display_value(value):
    return 'You have selected "{}"'.format(value)
    
if __name__ == '__main__':
    app.run_server(debug=True)  