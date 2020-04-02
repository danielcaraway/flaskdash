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


import plotly.graph_objects as go
import pandas as pd

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')


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

dftable.columns = ['Country,Other', 'TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths',
       'TotalRecovered', 'ActiveCases', 'Serious,Critical', 'TotPerM',
       'DeathsPerM', 'Reported1stcase']

dftable.loc[dftable['Country,Other'] == 'USA','Country,Other'] = 'United States'
dftable.loc[dftable['Country,Other'] == 'UK','Country,Other'] = 'United Kingdom'
dftable.loc[dftable['Country,Other'] == 'S. Korea','Country,Other'] = 'Korea, South'
dftable.loc[dftable['Country,Other'] == 'Czechia','Country,Other'] = 'Czech Republic'

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')

mydict = dict(zip(df.COUNTRY, df.CODE))
mydict_inverted = dict([[v,k] for k,v in mydict.items()])

def get_country_code(country):
    try:
        try:
            return mydict[country]
        except:
            return mydict_inverted[country]
    except:
        return 'no code'
    
dftable['CODE'] = dftable.apply(lambda x: get_country_code(x['Country,Other']), axis=1)
dftable['TOTAL'] = pd.to_numeric(dftable['TotalCases'].str.replace(',', ''), errors='coerce')
dftable['TOTAL_DEATHS'] = pd.to_numeric(dftable['TotalDeaths'].str.replace(',', ''), errors='coerce')
dftable['TOTAL_PER_1M'] = pd.to_numeric(dftable['TotPerM'].str.replace(',', ''),errors='coerce')
dftable['TOTAL_DEATHS_PER_1M'] = pd.to_numeric(dftable['DeathsPerM'].str.replace(',', ''),errors='coerce')

# dftable

df = dftable.copy()

fig2 = go.Figure(data=go.Choropleth(
    locations = df['CODE'],
    # locations = df['COUNTRY'],
    z = df['TOTAL'],
    text = df['Country,Other'],
    colorscale = 'Blues',
    autocolorscale=True,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix = '',
    colorbar_title = 'Current Cases',
))

fig2.update_layout(
    title_text='Coronavirus: Total Cases',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations = [dict(
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://www.worldometers.info/coronavirus/">\
            Worldometer</a>',
        showarrow = False
    )]
)


fig3 = go.Figure(data=go.Choropleth(
    locations = df['CODE'],
    # locations = df['COUNTRY'],
    z = df['TOTAL_DEATHS'],
    text = df['Country,Other'],
    colorscale = 'Blues',
    autocolorscale=True,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix = '',
    colorbar_title = 'Total Deaths',
))

fig3.update_layout(
    title_text='Coronavirus: Total Deaths',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations = [dict(
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://www.worldometers.info/coronavirus/">\
            Worldometer</a>',
        showarrow = False
    )]
)


fig4 = go.Figure(data=go.Choropleth(
    locations = df['CODE'],
    # locations = df['COUNTRY'],
    z = df['TOTAL_PER_1M'],
    text = df['Country,Other'],
    colorscale = 'Blues',
    autocolorscale=True,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix = '',
    colorbar_title = 'Cases Per 1M',
))

fig4.update_layout(
    title_text='Coronavirus: Total, Per 1M',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations = [dict(
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://www.worldometers.info/coronavirus/">\
            Worldometer</a>',
        showarrow = False
    )]
)

fig5 = go.Figure(data=go.Choropleth(
    locations = df['CODE'],
    # locations = df['COUNTRY'],
    z = df['TOTAL_DEATHS_PER_1M'],
    text = df['Country,Other'],
    colorscale = 'Blues',
    autocolorscale=True,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix = '',
    colorbar_title = 'Deaths Per 1M',
))

fig5.update_layout(
    title_text='Coronavirus: Total Deaths, Per 1M',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations = [dict(
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://www.worldometers.info/coronavirus/">\
            Worldometer</a>',
        showarrow = False
    )]
)

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
    html.H2('Global Coronavirus'),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3),
    dcc.Graph(figure=fig4),
    dcc.Graph(figure=fig5),
    html.H2('PICK A COUNTRY -- Coming Soon'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['USA', 'UK', 'China']],
        value='USA'
    ),
    html.Div(id='display-value')
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
            [dash.dependencies.Input('dropdown', 'value')])

def display_value(value):
    return 'You have selected "{}"'.format(value)
    
if __name__ == '__main__':
    app.run_server(debug=True)  