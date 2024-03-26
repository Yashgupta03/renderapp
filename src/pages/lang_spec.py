import plotly.express as px
import pandas as pd
import dash
from dash import Dash, dcc, Input, Output, html,callback, clientside_callback
import json
import numpy as np


dash.register_page(__name__,order=2)
df_data=pd.read_csv("data_refined.csv")
df_lang=pd.read_csv("lang_data.csv")
with open('assets/update.geojson') as response:
    geodata = json.loads(response.read())


@callback(
        Output("choro_lang", "figure"),
        [Input("major_lang_dropdown","value")]
)
def create_choro_specific(major_lang_dropdown):
    df_sp1=df_data.copy()
    df_sp1.loc[df_sp1["Languages"] != major_lang_dropdown, "Languages"] = "Not Selected"
    color_map={
        "Not Selected": 'White',
        major_lang_dropdown : 'Red',
    }
    fig = px.choropleth_mapbox(
                    df_sp1, 
                    geojson = geodata, 
                    locations = df_sp1.Districts, 
                    color = df_sp1["Languages"], 
                    color_discrete_map=color_map,
                    featureidkey = "properties.District",
                    mapbox_style = "carto-positron",
                    center = {"lat": 22.5937, "lon": 81.0629},
                    hover_name="STATE",
                    # hover_data=['STATE'],
                    zoom = 3.0,
                    opacity = 1.0,
                    )
    fig.update_layout(autosize=False,
                height=1000,
                width=1500,
                # title="Map for "+major_lang_dropdown,
                margin={"r":0,"t":100,"l":300,"b":0},
                )
    return fig


layout = html.Div([
    html.H1('This is our Language Specific page'),
    html.Br(),
    dcc.Dropdown(
                options=np.append(df_lang['Languages'].dropna().unique(),["NO CHOOSEN",]),
                value="NO CHOOSEN",
                id="major_lang_dropdown",
                style={"width": "40%"}
            ),
    dcc.Graph(id="choro_lang")
])