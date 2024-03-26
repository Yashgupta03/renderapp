import plotly.express as px
import pandas as pd
import dash
from dash import dcc, Input, Output, html,callback
import json
import numpy as np


dash.register_page(__name__,order=3)
df_data=pd.read_csv("data_refined.csv")
df_lang=pd.read_csv("lang_data.csv")
with open('assets/update.geojson') as response:
    geodata = json.loads(response.read())

color_map={
    "NO": 'Grey',
    "DRAVIDIAN":"Grey",
    "KHETRANI": 'Grey',
    "SINO TIBETAN":"Grey",
}
fig_gl = px.choropleth_mapbox(
                df_data, 
                geojson = geodata, 
                locations = df_data.Districts, 
                color = df_data["Languages"], 
                color_discrete_map=color_map,
                featureidkey = "properties.District",
                mapbox_style = "carto-positron",
                center = {"lat": 22.5937, "lon": 82.9629},
                hover_name="STATE",
                hover_data=['STATE'],
                zoom = 3.0,
                # opacity = 0.8,
                # labels={'unemp':'Languages'},
                )
fig_gl.update_layout(autosize=False,
            height=700,
            width=1000,
            margin={"r":0,"t":0,"l":0,"b":0},
            )
fig_gl.update_traces(marker_line_width=0.3)

layout = html.Div([
    html.H1('This is our Language Distribution page'),
    html.Br(),
    html.Div([html.Div([dcc.Graph(id="lang_map",figure=fig_gl),html.Br(),dcc.Dropdown(options=np.append(df_lang['Languages'].dropna().unique(),["NO CHOOSEN",]),
            value="NO CHOOSEN",
            placeholder="Select a Language",
            id="lang_dropdown",
            style={"width": "40%"}
        )],style={"display":"flex","flexDirection":"column"}),html.Div([dcc.Graph(id="dist_lang"),dcc.Graph(id="state_lang")],style={"display":"flex","flexDirection":"column"})],style={"display":"flex"})
])


@callback(
    Output("dist_lang", "figure"),
    [Input("lang_map", "clickData"),]
)
def create_graph(clickData,):
    if clickData is None:
        district_name = "DELHI_TOTAL"
    else:
        district_name = clickData["points"][0]["location"]

    dff = df_lang[df_lang["Districts"] == district_name]
    fig = px.line(dff, x="Districts", y="Languages", markers=True)
    return fig


@callback(
    Output("state_lang", "figure"),
    [Input("lang_map", "clickData"),
    Input("lang_dropdown","value")]
)
def create_graph1(clickData,lang_dropdown):
    if lang_dropdown!="NO CHOOSEN" :
        df1=df_lang[df_lang["Languages"] == lang_dropdown]
        fig = px.line(df1, x="Districts", y="Languages", markers=True)
        return fig
    if clickData is None:
        state_name = "DELHI"
    else:
        state_name = clickData["points"][0]["customdata"][0]

    dff = df_data[df_data["STATE"] == state_name]
    fig = px.line(dff, x="Districts", y="Languages", markers=True)
    return fig

@callback(
        Output("lang_dropdown","value"),
        Input("lang_map","clickData")
)
def update_prev_click(clickData):
    return  "NO CHOOSEN"
