import dash_echarts
import dash
from dash import html
from dash.exceptions import PreventUpdate
import tree_data

app = dash.Dash(__name__)

opts = {
    "tooltip": {
        "trigger": "item",
        "triggerOn": "mousemove",
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
events = {
    "click": "function(para) { window.open('https://www.google.com/maps/'); console.log(para.data.name );  return para.name}",
}
app.layout = html.Div([
    dash_echarts.DashECharts(
        option = opts,
        event=events,
        id='echarts',
        style={
            "width": '100vw',
            "height": '100vh',
        }
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)