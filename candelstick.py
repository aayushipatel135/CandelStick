import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import pandas as pd
  
# X = deque(maxlen = 20)
# X.append(1)
  
# Y = deque(maxlen = 20)
# Y.append(1)

df = pd.read_csv("data.csv")
df = df.set_index(pd.DatetimeIndex(df['Date']))
  
# app = dash.Dash(__name__)
# server = app.server
  
# app.layout = html.Div(
#     [
#         dcc.Graph(id = 'live-graph', animate = True),
#         dcc.Interval(
#             id = 'graph-update',
#             interval = 1000,
#             n_intervals = 0
#         ),
#     ]
# )
  
# @app.callback(
#     Output('live-graph', 'figure'),
#     [ Input('graph-update', 'n_intervals') ]
# )
  
# def update_graph_scatter(n):
#     X.append(X[-1]+1)
#     Y.append(Y[-1]+Y[-1] * random.uniform(-0.1,0.1))
  
#     data = plotly.Candlestick(
#                             	x = df.index,
#                             	low = df['Low'],
#                             	high = df['High'],
#                             	close = df['Adj Close'],
#                             	open = df['Open'],
#                             	increasing_line_color = 'green',
#                             	decreasing_line_color = 'red'
#         )
  
#     return {'data': [data],
#             'layout' : go.Layout( title="Stock Price",
#                     xaxis_title="Date",
#                     yaxis_title="Price",
#                     autosize=False,
#                     width=1800,
#                     height=800,
#                     margin=dict(l=30,r=30,b=30,
#                                 t=30,pad=3
#                                 ),
#                     paper_bgcolor="white")}
  
# if __name__ == '__main__':
#     app.run_server(debug=False)


last_id = 0

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    html.Div(className='container-fluid',children=
[
	html.Div(className='row', children=html.Div(dcc.Graph(id='live-graph', animate=True), className='col s12 m12 l12')),
	dcc.Interval(
		id='graph-update',
		interval=5000
	)
]),
)

@app.callback(
Output('live-graph','figure'),
events = [Event('graph-update','interval')]
)
def graph_update():
    global df

    ndf = df.iloc[0:2]
    print(ndf)

    last_id = ndf.iloc[0]['open_time']

    ndf['data'] = pd.to_datetime(ndf['open_time'], unit='ms')
    ndf.set_index('open_time', inplace=True)
    ndf.round({'close': 8, 'open': 8, 'high': 8, 'low': 8})

    data = [ dict(
        type = 'candlestick',
        open = ndf.open,
        high = ndf.high,
        low = ndf.low,
        close = ndf.close,
        x = ndf.data,
        yaxis = 'y2',
        name = 'Ripple',
    )]

    df = df.iloc[2:]
    print(df)

    return {'data': data, 'layout': {'title': str(last_id)}}

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_js:
    app.scripts.append_script({'external_url': js})

if __name__ == '__main__':
    app.run_server(debug=False)
