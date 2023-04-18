from dash import Dash, html, dcc, dash_table, Output, Input, State
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from .models import *
from zoneinfo import ZoneInfo
from django.conf import settings
from datetime import datetime, time, date


# when using bootstrap themes, you need to also load tailwind css to prevent bootstrap from overriding tailwind
load_figure_template("FLATLY")
external_script = ["https://tailwindcss.com/", {"src": "https://cdn.tailwindcss.com"}, dbc.themes.FLATLY]
app = DjangoDash("TableApp", external_scripts=external_script)

fish_names = list(TargetFishSpecies.objects.all().values_list('name', flat=True))
camera_names = list(CameraInfo.objects.all().values_list('name', flat=True))
analysis_types = ["每日通過魚道數", "魚道利用狀況"]

app.layout = html.Div([
    html.Div([
        html.Div(["選擇位置:", dcc.Dropdown(camera_names, camera_names[0], id='dropdown-camera')], className="grow"),
        html.Div(["選擇魚種:", dcc.Dropdown(fish_names, fish_names[0], id='dropdown-fish')], className="grow"),
        html.Div(["選擇時間範圍", 
                  dcc.DatePickerRange(
                      min_date_allowed=date(2023,1,1), 
                      max_date_allowed=datetime.today().date(),
                      start_date=(datetime.today() - timedelta(days=7)).date(),
                      end_date=datetime.today().date(), 
                      id='date-range')], className="grow md:col-start-4")
        ],className="flex flex-row gap-4 grid md:grid-cols-4"),
    html.Div("每日魚道通過數量", className="text-4xl mx-auto text-blue-600 text-center p-4"),
    dcc.Loading(id="loading", type="graph", children=html.Div("",id='table-content', className="w-[60vw] md:w-[40vw] mx-auto shadow-2xl rounded-sm bg-gray-100")),    
    html.Button("下載", id='download-button', className="my-4 bg-blue-500 hover:bg-blue-700 text-white font-bold px-8 rounded"),
    dcc.Download(id='download-table')
])


@app.callback(
    Output('table-content', 'children'),
    Input('dropdown-camera', 'value'),
    Input('dropdown-fish', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
    )
def update_table(camera_name, fish_name, start_date, end_date):
    query_set = FishCount.objects.filter(fish=fish_name, analysis__camera=camera_name, analysis__event_time__range=[start_date, end_date]).values_list('analysis__event_time', 'count')
    # query_set = FishCount.objects.filter(fish=fish_name, analysis__camera=camera_name).values_list('analysis__event_time', 'count')
    df = pd.DataFrame(list(query_set), columns=['event_time', 'count'])
    d = [d.astimezone(ZoneInfo(settings.TIME_ZONE)).date() for d in df['event_time']]
    df['event_time'] = d
    df = df.groupby('event_time').sum().reset_index()    
    df.columns = ['日期', '數量']    
    return dash_table.DataTable(
        data = df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        style_as_list_view=True,
        # filter_action='native',
        sort_action='native',
        page_size=25,
        fixed_rows={ 'headers': True},
        style_cell={'minWidth': '30px','width': '30px','maxWidth': '30px','font-size':"12px",'textAlign':'center'},
        style_header={'background':'rgb(109 40 217)','color':'#fff','font-weight':'600','border':'1px solid #000','border-radius': '2vh 2vh 0 0'},
        style_data={'whiteSpace': 'normal','height': 'auto'},
        style_table={'overflowY': 'auto'},
    )


@app.callback(
    Output("download-table", "data"),
    Input("download-button", "n_clicks"),
    State('dropdown-camera', 'value'),
    State('dropdown-fish', 'value'),
    State('date-range', 'start_date'),
    State('date-range', 'end_date'),
    prevent_initial_call=True,
)
def download_table(n_clicks, camera_name, fish_name, start_date, end_date):
    query_set = FishCount.objects.filter(fish=fish_name, analysis__camera=camera_name, analysis__event_time__range=[start_date, end_date]).values_list('analysis__event_time', 'count')
    df = pd.DataFrame(list(query_set), columns=['event_time', 'count'])
    d = [d.astimezone(ZoneInfo(settings.TIME_ZONE)).date() for d in df['event_time']]
    df['event_time'] = d
    df = df.groupby('event_time').sum().reset_index()    
    df.columns = ['日期', '數量']   
    return dcc.send_data_frame(df.to_csv, f"碧潭堰魚道通過數量_{camera_name}_{fish_name}_{start_date}-{end_date}.csv")