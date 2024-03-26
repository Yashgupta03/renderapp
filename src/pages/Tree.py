import plotly.express as px
import pandas as pd
import dash
from dash import Dash, dcc, Input, Output, html,callback
import dash_echarts
import tree_data
import numpy as np


dash.register_page(__name__,order=1,path='/')

opts = {
    "tooltip": {
        "trigger": "item",
        "triggerOn": "mousemove",
        'formatter': '{b}'
    },
    "series": [
        {
            "type": "tree",
            "data": [tree_data.data],
            "top": "1%",
            "left": "10%",
            "bottom": "1%",
            "right": "20%",
            "symbolSize": 7,
            "label": {
                "position": "bottom",
                "verticalAlign": "middle",
                "align": "right",
                "fontSize": 10,
                "color": "black",
            },
            "leaves": {
                "label": {
                    "position": "right",
                    "verticalAlign": "middle",
                    "align": "left",
                }
            },
            # "emphasis": {
            #     "focus": 'descendant'
            # },
            "expandAndCollapse": True,
            "animationDuration": 550,
            "animationDurationUpdate": 750,
        },
        
    ],
}

fig_gt=dash_echarts.DashECharts(
    option = opts,
    id='echarts',
    style={
        "width": '100vw',
        "height": '100vh',
    }
)

layout = html.Div([
    html.H1('This is our Tree page'),
    html.Br(),
    html.Div(id="tree",children=[fig_gt])
])
