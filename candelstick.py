from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd


app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H4('Apple stock candlestick chart'),
    dcc.Checklist(
        id='toggle-rangeslider',
        options=[{'label': 'Include Rangeslider', 
                  'value': 'slider'}],
        value=['slider']
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"), 
    Input("toggle-rangeslider", "value"))
def display_candlestick(value):
    df = pd.read_csv('data.csv') # replace with your own data source
    fig = go.Figure(go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Adj Close']
    ))

    fig.update_layout(
        xaxis_rangeslider_visible='slider' in value
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=False)

# app.run_server(debug=True)
# import dash
# from dash.dependencies import Output, Input
# import dash_core_components as dcc
# import dash_html_components as html
# import plotly
# import random
# import plotly.graph_objs as go
# from collections import deque
# import pandas as pd

# df = pd.read_csv("data.csv")
# df = df.set_index(pd.DatetimeIndex(df['Date']))

# app = dash.Dash(__name__)
# server = app.server
  
# app.layout = html.Div(
#     [
#         html.H1(id = "count-up"),
#         dcc.Graph(id = 'candles'),
#         dcc.Interval(
#             id = 'graph-update',
#             interval = 2000,
#            # n_intervals = 0
#         ),
#     ]
# )
  
# # @app.callback(
# #     Output('live-graph', 'figure'),
# #     [ Input('graph-update', 'n_intervals') ]
# # )
# @app.callback(
#   Output("candles","figure"),
#   Input("interval","n_intervals"),
# )
  
# def update_graph_scatter(n_intervals):
#     url = "https://www.bitstamp.net/api/v2/ohlc/btcusd/"
#     params = { "step" : "60",
#                 "limit" : "30",}
#     data = request.get(url,params = params).json()["data"]["ohlc"]
#     data.timestamp = pd.to_datetime(data.timestamp,unit="s")
#     candles = go.Figure(
#       data = plotly.Candlestick(
#                   x = data.timestamp,
#                   low = data.low,
#                   high = data.high,
#                   close = data.close,
#                   open = data.open,
#                   # increasing_line_color = 'green',
#                   # decreasing_line_color = 'red'
#           )
#     )
#     # candles = go.Figure(
#     #   data = plotly.Candlestick(
#     #               x = df.index,
#     #               low = df['Low'],
#     #               high = df['High'],
#     #               close = df['Adj Close'],
#     #               open = df['Open'],
#     #               increasing_line_color = 'green',
#     #               decreasing_line_color = 'red'
#     #       )
#     # )
#     return candles
  
# if __name__ == '__main__':
#     app.run_server(debug=False)
