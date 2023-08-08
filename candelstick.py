import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import pandas as pd
  
X = deque(maxlen = 20)
X.append(1)
  
Y = deque(maxlen = 20)
Y.append(1)

df = pd.read_csv("data.csv")
df = df.set_index(pd.DatetimeIndex(df['Date']))
  
app = dash.Dash(__name__)
server = app.server
  
app.layout = html.Div(
    [
        dcc.Graph(id = 'live-graph', animate = True),
        dcc.Interval(
            id = 'graph-update',
            interval = 1000,
            n_intervals = 0
        ),
    ]
)
  
@app.callback(
    Output('live-graph', 'figure'),
    [ Input('graph-update', 'n_intervals') ]
)
  
def update_graph_scatter(n):
    X.append(X[-1]+1)
    Y.append(Y[-1]+Y[-1] * random.uniform(-0.1,0.1))
  
    data = plotly.Candlestick(
                            	x = df.index,
                            	low = df['Low'],
                            	high = df['High'],
                            	close = df['Adj Close'],
                            	open = df['Open'],
                            	increasing_line_color = 'green',
                            	decreasing_line_color = 'red'
        )
  
    return {'data': [data],
            'layout' : go.Layout( title="Stock Price",
                    xaxis_title="Date",
                    yaxis_title="Price",
                    autosize=False,
                    width=1800,
                    height=800,
                    margin=dict(l=30,r=30,b=30,
                                t=30,pad=3
                                ),
                    paper_bgcolor="white")}
  
if __name__ == '__main__':
    app.run_server(debug=False)
