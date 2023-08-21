from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from .models import *
from zoneinfo import ZoneInfo
from django.conf import settings
from datetime import datetime, date, time


# when using bootstrap themes, you need to also load tailwind css to prevent bootstrap from overriding tailwind
load_figure_template("FLATLY")
external_script = ["https://tailwindcss.com/", {"src": "https://cdn.tailwindcss.com"}, dbc.themes.FLATLY]
app = DjangoDash("PlotApp", external_scripts=external_script)

fish_names = list(TargetFishSpecies.objects.all().values_list("name", flat=True))
camera_names = list(CameraInfo.objects.all().values_list("name", flat=True))
if camera_names:
    default_camera_name = camera_names[0]
else:
    default_camera_name = "No camera"
if fish_names:
    default_fish_name = fish_names[0]
else:
    default_fish_name = "No fish name"

analysis_types = ["每日魚道通過數", "每小時魚道使用狀況"]


app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    ["選擇位置:", dcc.Dropdown(camera_names, default_camera_name, id="dropdown-camera")], className="grow"
                ),
                html.Div(
                    ["分析類型:", dcc.Dropdown(analysis_types, analysis_types[0], id="dropdown-analysis")],
                    className="grow",
                ),
                html.Div(
                    [
                        "選擇時間範圍",
                        dcc.DatePickerRange(
                            min_date_allowed=date(2023, 1, 1),
                            max_date_allowed=datetime.today().date(),
                            start_date=(datetime.today() - timedelta(days=7)).date(),
                            end_date=datetime.today().date(),
                            id="date-range",
                        ),
                    ],
                    className="grow md:col-start-4",
                ),
            ],
            className="flex flex-row gap-4 grid md:grid-cols-4",
        ),
        html.Div("每日魚道通過數量", className="text-4xl mx-auto text-blue-600 text-center p-4", id="title"),
        dcc.Loading(
            id="loading",
            type="graph",
            children=html.Div(
                dcc.Graph(
                    figure=px.line(x=range(10), y=range(10)),
                    id="graph-content",
                    config={"displayModeBar": False},
                    className="w-full shadow-2xl rounded-sm bg-gray-100",
                )
            ),
        ),
    ]
)


@app.callback(
    Output("graph-content", "figure"),
    Output("title", "children"),
    Input("dropdown-camera", "value"),
    Input("dropdown-analysis", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_graph(camera_name, analysis_type, start_date, end_date):
    if analysis_type == "每日魚道通過數":
        query_set = PassCount.objects.filter(
            analysis__camera=camera_name, analysis__event_date__range=[start_date, end_date]
        ).values_list("analysis__event_date", "fish", "count")
        df = pd.DataFrame(list(query_set), columns=["event_date", "fish", "count"])
        fig = px.line(
            df,
            x="event_date",
            y="count",
            color="fish",
            labels={"event_date": "觀測日期", "count": "隻數", "fish": "魚種類群"},
        )
        return fig, "每日魚道通過數"
    else:
        query_set = FishwayUtility.objects.filter(
            analysis__camera=camera_name, analysis__event_date__range=[start_date, end_date]
        ).values_list("analysis__event_date", "hour", "fish", "count")
        if len(query_set) == 0:
            return {}, "無資料"
        df = pd.DataFrame(list(query_set), columns=["event_date", "hour", "fish", "count"])
        # ref from: https://stackoverflow.com/questions/64246528/add-missing-rows-based-on-column
        df = df.merge(
            pd.DataFrame(
                index=pd.MultiIndex.from_product([df["event_date"].unique(), df["hour"].unique(), df["fish"].unique()])
            ),
            left_on=["event_date", "hour", "fish"],
            right_index=True,
            how="outer",
        ).fillna(0)
        df["event_time"] = [datetime.combine(d, time(hour=h)) for d, h in zip(df["event_date"], df["hour"])]
        df = df.sort_values(by=["event_time", "fish"])
        fig = px.line(
            df,
            x="event_time",
            y="count",
            color="fish",
            labels={"event_time": "觀測時段", "count": "平均隻數", "fish": "魚種類群"},
        )
        return fig, "每小時魚道使用狀況"
