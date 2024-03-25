import plotly.express as px
import pandas as pd
from dash import Dash, dcc, Input, Output, html
import json


df_data=pd.read_csv("data_refined.csv")
df_lang=pd.read_csv("lang_data.csv")
with open('refined.geojson') as response:
    geodata = json.load(response)

app = Dash(__name__)
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

    html.Div(dcc.Graph(id="lang_map")),

    html.Br(),

    dcc.Graph(id="dist_lang",style={'display':'inline-block'}),
    dcc.Graph(id="state_lang",style={'display':'inline-block'})

])

@app.callback(
    Output("lang_map", "figure"),
    Input("dataframe_dropdown", "value")
)
def choropleth_map(dataframe_dropdown):
    fig = px.choropleth_mapbox(
                    # df_data, 
                    # geojson = geodata, 
                    # locations = df_data.Districts, 
                    # color = [255,255,255], 
                    # featureidkey = "properties.District",
                    mapbox_style = "carto-positron",
                    center = {"lat": 22.5937, "lon": 82.9629},
                    # hover_name="STATE",
                    # hover_data=['STATE'],
                    zoom = 3.0,
                    opacity = 1.0
                    )
    fig.update_layout(autosize=False,
                height=700,
                width=600,
                margin={"r":0,"t":0,"l":0,"b":0})

    return fig

@app.callback(
    Output("dist_lang", "figure"),
    Input("lang_map", "clickData"),
    # Input("lang_map", "hoverData"),
    Input("dataframe_dropdown", "value"),
)
def create_graph(clickData, dataframe_dropdown):
    print(clickData)
    if clickData is None:
        district_name = "GHAZIABAD"
    else:
        district_name = clickData["points"][0]["location"]

    dff = df_lang[df_lang["Districts"] == district_name]
    fig = px.line(dff, x="Districts", y="Languages", markers=True)
    fig.update_layout(width=600)
    return fig

@app.callback(
    Output("state_lang", "figure"),
    Input("lang_map", "clickData"),
    # Input("lang_map", "hoverData"),
    Input("dataframe_dropdown", "value"),
)
def create_graph(clickData, dataframe_dropdown):
    print(clickData)
    if clickData is None:
        state_name = "RAJASTHAN"
    else:
        state_name = clickData["points"][0]["customdata"][0]

    dff = df_data[df_data["STATE"] == state_name]
    fig = px.line(dff, x="Districts", y="Languages", markers=True)
    fig.update_layout(width=800)

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
