import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import pandas as pd
# import talib


df = pd.read_csv('data1.csv')
df = df.set_index(pd.DatetimeIndex(df['Date']))
# df["SMA"] = talib.SMA(df.Close, timeperiod=3)
# df["RSI"] = talib.RSI(df.Close, timeperiod=3)
# df["EMA"] = talib.EMA(df.Close, timeperiod=3)


x = deque(maxlen = 30)
x.append(df.iloc[0,0])

open = deque(maxlen = 30)
open.append(df.iloc[0,1])

high = deque(maxlen = 30)
high.append(df.iloc[0,2])

low = deque(maxlen = 30)
low.append(df.iloc[0,3])

close = deque(maxlen = 30)
close.append(df.iloc[0,4])

mid = deque(maxlen = 30)
mid.append((df.iloc[0,4] - df.iloc[0,1])/2)

# ema = deque(maxlen = 20)
# ema.append(df.iloc[0,9])

# sma = deque(maxlen = 20)
# sma.append(df.iloc[0,7])


X = deque(maxlen = 30)
X.append(1)

Y = deque(maxlen = 30)
Y.append(1)

last = len(df) - 1

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
    global last
    if last > 0 : 
            x.append(df.iloc[last,0])
            open.append(df.iloc[last,1])
            high.append(df.iloc[last,2])
            low.append(df.iloc[last,3])
            close.append(df.iloc[last,4])
            mid.append((df.iloc[last,4] - df.iloc[last,1])/2)
    
            candle = plotly.graph_objs.Candlestick(
                    x = list(x),
                    low = list(low),
                    high = list(high),
                    close = list(close),
                    open = list(open),
                    increasing_line_color = 'green',
                    decreasing_line_color = 'red'
            )
            scatter = plotly.graph_objs.Scatter(
                x=list(x),
                y=list(open),
                name='Scatter',
                mode= 'lines+markers'
            )
            last = last + 1
            return {'data': [candle,scatter],
                    'layout' : go.Layout(xaxis_rangeslider_visible=True,
                                         xaxis=dict(range=[min(x),max(x)]),
                                         yaxis=dict(range=[  min( low  )   ,   max(high)  ] ),
                                        )}
    else : 
        X.append(X[-1]+1)
        Y.append(Y[-1]+Y[-1] * random.uniform(-0.1,0.1))
        data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
        )
        return {'data': [data],
                'layout' : go.Layout(xaxis=dict(range=[min(X),max(X)]),yaxis = dict(range = [min(Y),max(Y)]),)}
        



if __name__ == '__main__':
    app.run_server(debug=False)

# from dash import Dash, dcc, html, Input, Output
# import plotly.graph_objects as go
# import pandas as pd

# df = pd.read_csv('data.csv')

# app = Dash(__name__)
# server = app.server

# app.layout = html.Div([
#     html.H4('Apple stock candlestick chart'),
#     dcc.Checklist(
#         id='toggle-rangeslider',
#         options=[{'label': 'Include Rangeslider', 
#                   'value': 'slider'}],
#         value=['slider']
#     ),
#     dcc.Graph(id="graph"),
# ])


# @app.callback(
#     Output("graph", "figure"), 
#     Input("toggle-rangeslider", "value"))
# def display_candlestick(value):
#      # replace with your own data source
#     fig = go.Figure(go.Candlestick(
#         x=df['Date'],
#         open=df['Open'],
#         high=df['High'],
#         low=df['Low'],
#         close=df['Adj Close']
#     ))

#     fig.update_layout(
#         xaxis_rangeslider_visible='slider' in value
#     )

#     return fig

# if __name__ == '__main__':
#     app.run_server(debug=False)
  
# if __name__ == '__main__':
#     app.run_server(debug=False)
