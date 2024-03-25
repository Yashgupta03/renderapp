import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from pydeck.types import String
import dash
import dash_deck
import plotly.express as px
from dash import Dash, dcc, Input, Output, html
import json

df = pd.read_json("../test2.json")
df1 = pd.read_json("../test4.json")
df_data=pd.read_csv("data_refined.csv")
with open('test.geojson') as response:
    geodata = json.load(response)
dict1={'html': 
       '<b>Language:</b> {val}' 
       '<div class="piechart">yash</div>'
       '''<style> 
		.piechart { 
			margin-top: 0px; 
			display: block; 
			position: absolute; 
			width: 40px; 
			height: 40px; 
			border-radius: 50%; 
			background-image: {pie}; 
		} 

		body, 
		.piechart { 
			display: flex; 
			justify-content: center; 
			align-items: center; 
		} 
	</style>''' 
       }
r=pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=20.5937,
        longitude=78.9629,
        zoom=4,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            "TextLayer",
            df,
            pickable=True,
            get_position="coordinates",
            get_text="name",
            get_size=16,
            get_color=[0, 0, 0],
            get_angle="degree",
            # sdf=True,
            get_radius=30,
            # Note that string constants in pydeck are explicitly passed as strings
            # This distinguishes them from columns in a data set
            get_text_anchor=String("middle"),
            get_alignment_baseline=String("center"),
        ),
        pdk.Layer(
            "PathLayer",
            df1,
            pickable=True,
            get_path="path",
            get_color="color",
            width_scale=20,
            width_min_pixels=2,
            get_width=5,
        )
    ],
    # tooltip=dict1,
)

fig = px.choropleth_mapbox(
                    df_data, 
                    geojson = geodata, 
                    locations = df_data.Districts, 
                    # color = [255,255,255], 
                    featureidkey = "properties.District",
                    mapbox_style = "carto-positron",
                    center = {"lat": 22.5937, "lon": 82.9629},
                    hover_name="STATE",
                    hover_data=['STATE'],
                    zoom = 3.0,
                    opacity = 1.0
                    )

deck_component = dash_deck.DeckGL(r.to_json(), id="deck-gl")

app = dash.Dash(__name__)
app.layout = html.Div(dcc.Graph(figure = fig))

if __name__ == "__main__":
    app.run_server(debug=True)