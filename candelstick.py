import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import pandas as pd

df = pd.read_csv("data.csv")
df = df.set_index(pd.DatetimeIndex(df['Date']))

app = dash.Dash(__name__)
server = app.server
  
app.layout = html.Div(
    [
        html.H1(id = "count-up"),
        dcc.Graph(id = 'candles'),
        dcc.Interval(
            id = 'graph-update',
            interval = 2000,
           # n_intervals = 0
        ),
    ]
)
  
# @app.callback(
#     Output('live-graph', 'figure'),
#     [ Input('graph-update', 'n_intervals') ]
# )
@app.callback(
  Output("candles","figure"),
  Input("interval","n_intervals"),
)
  
def update_graph_scatter(n_intervals):
    candles = go.Figure(
      data = plotly.Candlestick(
                  x = df.index,
                  low = df['Low'],
                  high = df['High'],
                  close = df['Adj Close'],
                  open = df['Open'],
                  increasing_line_color = 'green',
                  decreasing_line_color = 'red'
          )
    )
    return candles
  
if __name__ == '__main__':
    app.run_server(debug=False)
