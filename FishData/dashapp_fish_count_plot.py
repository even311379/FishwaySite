from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from .models import *
from zoneinfo import ZoneInfo
from django.conf import settings
from datetime import datetime, time


# when using bootstrap themes, you need to also load tailwind css to prevent bootstrap from overriding tailwind
load_figure_template("FLATLY")
external_script = ["https://tailwindcss.com/", {"src": "https://cdn.tailwindcss.com"}, dbc.themes.FLATLY]
app = DjangoDash("PlotApp", external_scripts=external_script)

fish_names = list(TargetFishSpecies.objects.all().values_list('name', flat=True))
camera_names = list(CameraInfo.objects.all().values_list('name', flat=True))
analysis_types = ["每日通過魚道數", "魚道利用狀況"]

app.layout = html.Div([
    html.Div([
        html.Div(["選擇位置:", dcc.Dropdown(camera_names, camera_names[0], id='dropdown-camera')], className="grow"),
        html.Div(["選擇魚種:", dcc.Dropdown(fish_names, fish_names[0], id='dropdown-fish')], className="grow"),
        html.Div(["分析類型:", dcc.Dropdown(analysis_types, analysis_types[0], id='dropdown-analysis')], className="grow md:col-start-4")],
             className="flex flex-row gap-4 grid md:grid-cols-4"),
    html.Div("每日魚道通過數量", className="text-4xl mx-auto text-blue-600 text-center p-4", id='title'),
    dcc.Loading(id="loading", type="graph", children=html.Div(
        dcc.Graph(figure=px.line(x=range(10), y = range(10)),id='graph-content', className="w-full shadow-2xl rounded-sm bg-gray-100"))
    )
])


## TODO: the whole process takes too much time... maybe precompute these values and store in database?

@app.callback(
    Output('graph-content', 'figure'),
    Output('title', 'children'),
    Input('dropdown-camera', 'value'),
    Input('dropdown-fish', 'value'),
    Input('dropdown-analysis', 'value'))
def update_graph(camera_name, fish_name, analysis_type):
    if analysis_type == "每日通過魚道數":
        query_set = FishCount.objects.filter(fish=fish_name, analysis__camera=camera_name).values_list('analysis__event_time', 'count')
        df = pd.DataFrame(list(query_set), columns=['event_time', 'count'])
        d = [d.astimezone(ZoneInfo(settings.TIME_ZONE)).date() for d in df['event_time']]
        df['event_time'] = d
        df = df.groupby('event_time').sum().reset_index()
        return px.line(df, x='event_time', y='count'), "每日魚道通過數量"
    else:
        query_set = FishDetection.objects.filter(fish=fish_name).values_list('analysis__event_time', 'detect_time', 'count')
        if len(query_set) == 0:
            return {}, "無資料"
        # make it per hour histogram
        df = pd.DataFrame(list(query_set), columns=['event_time', 'detect_time', 'count'])
        dt = [d.astimezone(ZoneInfo(settings.TIME_ZONE)) + timedelta(hours=t.hour - 6, minutes=t.minute, seconds=t.second) for d, t in zip(df['event_time'], df['detect_time'])]
        df.drop(columns='event_time', inplace=True)
        df['detect_time'] = dt        
        df = df.groupby([df['detect_time'].dt.date, df['detect_time'].dt.hour]).mean()
        df.index.names = ['date', 'hour']
        df.reset_index(inplace=True)
        dt = [datetime.combine(d, time(hour=h)) for d, h in zip(df['date'], df['hour'])]
        df['detect_time'] = dt
        
        # fill zero...
        # get start and end date
        dl = FishAnalysis.objects.filter(camera=camera_name, analysis_type="DE").values_list('event_time', flat=True)
        dl = list(set(dl))
        dl = [d.astimezone(ZoneInfo(settings.TIME_ZONE)).date() for d in dl]
        fill_date = []
        fill_hour = []
        fill_detect_time = []
        for d in dl:
            hour_list = df[df['date'] == d].hour.tolist()
            for h in range(5, 20): # should depend on the actual case.... NEED MODIFY LATER
                if h in hour_list:
                    continue
                fill_date.append(d)
                fill_hour.append(h)
                fill_detect_time.append(datetime.combine(d, time(hour=h)))
        fill_df = pd.DataFrame({'date': fill_date, 'hour': fill_hour, 'detect_time': fill_detect_time, 'count': [0]*len(fill_date)})
        df = pd.concat([df, fill_df], ignore_index=True)
        df.sort_values(by=['detect_time'], inplace=True)
        fig = px.area(df, x='detect_time', y='count')
        # fig.update_layout(bargap=0)
        return fig, "魚道利用狀況"
