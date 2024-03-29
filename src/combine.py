import plotly.express as px
import pandas as pd
from dash import Dash, dcc, Input, Output, html
import json
import dash_echarts
import tree_data
import home_page
import numpy as np
import flask
from pathlib import Path


HERE = Path(__file__).parent

df_refined=pd.read_csv("data_refined.csv")
df_dialects=pd.read_csv("lang_dialects.csv")
with open('assets/update.geojson') as response:
    geodata = json.loads(response.read())

app = Dash(__name__)
server=app.server
app.config.suppress_callback_exceptions=True
app.layout = html.Div(children=[
    html.Div(className="row", children=[

        html.Div(className="six columns", children=[html.Label(['Mode:']),
            dcc.Dropdown(
                options=["Home Page","Language Tree","Language Specific","Language Distribution"],
                value="Home Page",
                id="dataframe_dropdown",
                style={"width": "40%"}
            )
        ])
    ]),
    html.Br(),
    html.A(html.Button("Physical Map"), href="/get_report", target="_blank"),

    html.Br(),
    html.Div(id="img")
])

@app.server.route("/get_report")
def get_report():
    return flask.send_from_directory(HERE, "physical_streamlit.html")

color_map={
    "NO": 'Grey',
    "DRAVIDIAN":"Grey",
    "KHETRANI": 'Grey',
    "SINO TIBETAN":"Grey",
}
fig_gl = px.choropleth_mapbox(
                df_refined, 
                geojson = geodata, 
                locations = df_refined.Districts, 
                color = df_refined["Languages"], 
                color_discrete_map=color_map,
                featureidkey = "properties.District",
                mapbox_style = "carto-positron",
                center = {"lat": 22.5937, "lon": 82.9629},
                hover_name="STATE",
                hover_data=['STATE'],
                zoom = 3.0
                )
fig_gl.update_layout(autosize=False,
            height=700,
            width=1000,
            margin={"r":0,"t":0,"l":0,"b":0},
            )
fig_gl.update_traces(marker_line_width=0.3)
h_choro=dcc.Graph(id="lang_map",figure=fig_gl)
h_g1=dcc.Graph(id="dist_lang")
h_g2=dcc.Graph(id="state_lang")
h_b1=html.Div([html.Label(['Language:']),dcc.Dropdown(options=np.append(df_refined['Languages'].dropna().unique(),["NO CHOOSEN",]),
            value="NO CHOOSEN",
            placeholder="Select a Language",
            id="lang_dropdown",
            style={"width": "40%"}
        )])

h_b2=html.Div([html.Label(['Districts:']),dcc.Dropdown(options=np.append(df_refined['Districts'].dropna().unique(),["NO CHOOSEN",]),
            value="NO CHOOSEN",
            placeholder="Select a District",
            id="district_dropdown",
            style={"width": "40%"}
        )])
h_d1=html.Div([h_choro,html.Br(),h_b1,html.Br(),h_b2],style={"display":"flex","flexDirection":"column"})
h_d2=html.Div([h_g1,h_g2],style={"display":"flex","flexDirection":"column"})
h_d3=html.Div([h_d1,h_d2],style={"display":"flex"})

def generate_tree():
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
    fig=dash_echarts.DashECharts(
        option = opts,
        id='echarts',
        style={
            "width": '100vw',
            "height": '100vh',
        }
    )
    return fig

def generate_choro_specific():
    return [html.Label(['Language:']),dcc.Dropdown(
                options=np.append(df_refined['Languages'].dropna().unique(),["NO CHOOSEN",]),
                value="NO CHOOSEN",
                id="major_lang_dropdown",
                style={"width": "40%"}
            ),html.Div([dcc.Graph(id="choro_lang"),dcc.Graph(id="dialect_dist")],style={"display":"flex"})]

@app.callback(
        Output("choro_lang", "figure"),
        [Input("major_lang_dropdown","value")]
)
def create_choro_specific(major_lang_dropdown):
    df_sp1=df_refined.copy()
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
                    zoom = 3.0,
                    opacity = 1.0,
                    )
    fig.update_layout(autosize=False,
                height=700,
                width=1000,
                margin={"r":0,"t":0,"l":0,"b":0},
                )
    return fig

@app.callback(
        Output("dialect_dist", "figure"),
        [Input("major_lang_dropdown","value")]
)
def create_graph2(major_lang_dropdown):
    dff = df_dialects[df_dialects["Dialect Name"] == major_lang_dropdown]
    t="Dialects vs Districts for language: "+major_lang_dropdown
    fig = px.scatter(dff, x="Districts", y="Dialects",hover_name="Dialect Name",title=t)
    return fig


@app.callback(
    Output("dist_lang", "figure"),
    [Input("lang_map", "clickData"),
    Input("dataframe_dropdown", "value")]
)
def create_graph(clickData,dataframe_dropdown):
    if dataframe_dropdown=="Language Tree":
        return 
    if clickData is None:
        district_name = "DELHI_TOTAL"
    else:
        district_name = clickData["points"][0]["location"]

    dff = df_dialects[df_dialects["Districts"] == district_name]
    fig = px.scatter(dff, x="Dialects", y="Dialect Name",hover_name="Dialect Name")
    return fig

@app.callback(
        Output("lang_dropdown","value"),
        Input("lang_map","clickData"),
        Input("district_dropdown","value")
)
def update_lang_dropdown(clickData,district_dropdown):
    return  "NO CHOOSEN"

@app.callback(
        Output("district_dropdown","value"),
        Input("lang_map","clickData")
)
def update_district_dropdown(clickData):
    return  "NO CHOOSEN"

@app.callback(
    Output("state_lang", "figure"),
    [Input("lang_map", "clickData"),
    Input("dataframe_dropdown", "value"),
    Input("lang_dropdown","value"),
    Input("district_dropdown","value")
    ]
)
def create_graph1(clickData,dataframe_dropdown,lang_dropdown,district_dropdown):
    if dataframe_dropdown=="Language Tree":
        return 
    elif lang_dropdown!="NO CHOOSEN" :
        dff = df_dialects[df_dialects["Dialect Name"] == lang_dropdown]
        fig = px.scatter(dff, x="Districts", y="Dialects",hover_name="Dialect Name")
        return fig
    elif district_dropdown!="NO CHOOSEN" :
        state_name=df_refined.loc[df_refined['Districts'] == district_dropdown, 'STATE'].iloc[0]
        dff = df_refined[df_refined["STATE"] == state_name]
        fig = px.scatter(dff, x="Districts", y="Languages",hover_name="Languages")
        return fig
    if clickData is None:
        state_name = "DELHI"
    else:
        state_name = clickData["points"][0]["customdata"][0]

    dff = df_refined[df_refined["STATE"] == state_name]
    fig = px.scatter(dff, x="Districts", y="Languages",hover_name="Languages")

    return fig

@app.callback(
    Output("img", "children"),
    Input("dataframe_dropdown", "value")
)
def update(dataframe_dropdown):
    if dataframe_dropdown=="Home Page":
        return home_page.h_home_page
    elif dataframe_dropdown=="Language Tree":
        return generate_tree()
    elif dataframe_dropdown=="Language Distribution":
        return h_d3
    else:
        return generate_choro_specific()

if __name__ == "__main__":
    app.run_server(debug=True)
