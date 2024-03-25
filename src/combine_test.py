import plotly.express as px
import pandas as pd
from dash import Dash, dcc, Input, Output, html, callback, ctx
import json
import dash_echarts
from dash.exceptions import PreventUpdate
import tree_data

df_data=pd.read_csv("data_refined.csv")
df_lang=pd.read_csv("lang_data.csv")
with open('refined.geojson') as response:
    geodata = json.load(response)

app = Dash(__name__)
app.config.suppress_callback_exceptions=True
app.layout = html.Div(children=[
    html.Div(className="row", children=[

        html.Div(className="six columns", children=[
            dcc.Dropdown(
                options=["not show","show"],
                value="show",
                id="dataframe_dropdown",
                style={"width": "40%"}
            )
        ])
    ]),

    html.Br(),

    html.Div(id="img"),
    html.Div(id="img1"),
    html.Div(id="img2"),
])

def generate_choro():
    fig = px.choropleth_mapbox(
                    df_data, 
                    geojson = geodata, 
                    locations = df_data.Districts, 
                    color = df_data["Languages"], 
                    featureidkey = "properties.District",
                    mapbox_style = "carto-positron",
                    center = {"lat": 22.5937, "lon": 82.9629},
                    hover_name="STATE",
                    hover_data=['STATE'],
                    zoom = 3.0,
                    opacity = 1.0
                    )
    fig.update_layout(autosize=False,
                height=700,
                width=600,
                margin={"r":0,"t":0,"l":0,"b":0})

    return dcc.Graph(id="lang_map",figure=fig)
    
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
    fig_tr=dash_echarts.DashECharts(
        option = opts,
        id='echarts',
        style={
            "width": '100vw',
            "height": '100vh',
        }
    )
    return fig_tr

@app.callback(
    Output("img1", "children"),
    [Input("dataframe_dropdown", "value"),
    Input("lang_map", "clickData")]
)
def create_graph(dataframe_dropdown,clickData):
    if dataframe_dropdown=="show":
        return html.Br()
    print(clickData)
    if clickData is None:
        district_name = "GHAZIABAD"
    else:
        district_name = clickData["points"][0]["location"]

    dff = df_lang[df_lang["Districts"] == district_name]
    fig = px.line(dff, x="Districts", y="Languages", markers=True)
    fig.update_layout(width=600)
    return dcc.Graph(id="dist_lang",style={'display':'inline-block'},figure=fig)

@app.callback(
    Output("img2", "children"),
    [Input("dataframe_dropdown", "value"),
    Input("lang_map", "clickData")]
)
def create_graph1(dataframe_dropdown,clickData):
    if dataframe_dropdown=="show":
        return html.Br()
    print(clickData)
    if clickData is None:
        state_name = "RAJASTHAN"
    else:
        state_name = clickData["points"][0]["customdata"][0]

    dff = df_data[df_data["STATE"] == state_name]
    fig = px.line(dff, x="Districts", y="Languages", markers=True)
    fig.update_layout(width=800)
    return dcc.Graph(id="state_lang",style={'display':'inline-block'},figure=fig)

@app.callback(
    Output("img", "children"),
    Input("dataframe_dropdown", "value"),
)
def update(dataframe_dropdown):
    if dataframe_dropdown=="show":
        return generate_tree()
    else:
        return generate_choro()

if __name__ == "__main__":
    app.run_server(debug=True)
