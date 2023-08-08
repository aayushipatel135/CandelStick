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

last = 0  
  
app = dash.Dash(__name__)
server = app.server
  
app.layout = html.Div(
    [
        dcc.H1(id = "count-up"),
        dcc.Graph(id = 'candels'),
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
  Input("interval","n_intervals"),
  Output("candels","children"),
)
  
def update_graph_scatter(n_intervals):
    global last
    df1 = df.iloc[last,:]  
    candels = go.Figure(
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
    candels.update_layout(
                    title="Stock Price",
                    xaxis_title="Date",
                    yaxis_title="Price",
                    autosize=False,
                    width=1800,
                    height=800,
                    margin=dict(l=30,r=30,b=30,
                                t=30,pad=3
                                ),
                    paper_bgcolor="white",
                )
    last = last + 1
    return candels
  
if __name__ == '__main__':
    app.run_server(debug=False)
