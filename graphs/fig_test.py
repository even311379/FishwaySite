from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

load_figure_template("FLATLY")

app = DjangoDash("TestApp", external_stylesheets=[dbc.themes.FLATLY])


# app = Dash("TestApp")

app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dcc.Graph(figure=px.line(x=range(10), y = range(10)),id='graph-content')
])

@app.callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    print(value)
    dff = df[df.country==value]
    return px.line(dff, x='year', y='pop')

