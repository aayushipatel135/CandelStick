import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import pandas as pd
import dash_daq as daq
from flask import request


df = pd.read_csv('working.csv')
x = []
x.append(df.iloc[0,0])
open = []
open.append(df.iloc[0,4])
high = []
high.append(df.iloc[0,2])
low = []
low.append(df.iloc[0,3])
close = []
close.append(df.iloc[0,1])
last = 0
time_interval = 1500


# Initialising variables
X, y = [], []
X.append(0); y.append(1)

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    daq.ToggleSwitch(
        id='my-toggle-switch',
        value=False
    ),
    html.Div(id='toggle-switch-output'),

    dcc.Graph(id='live-graph', animate=False),
            dcc.Interval(
                id='graph-update',
                interval=time_interval
            ),
])


@app.callback(
    [Output('toggle-switch-output', 'children'),
     Output('live-graph', 'figure')],
    [Input('my-toggle-switch', 'value'),
     Input('graph-update', 'n_intervals')])

def update_output(value,data):
    global last
    global time_interval

    X.append(X[-1] + 1)
    y.append(y[-1] + y[-1] * random.uniform(-0.1, 0.1))

    string1 = 'The switch is off'
    string2 = 'This is working'

    fig1 = go.Figure()
    fig1.update_layout(plot_bgcolor='rgba(255,255,255,255)', paper_bgcolor='rgba(255,255,255,255)',
                      yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color='rgba(255,255,255,255)')),
                      xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color='rgba(255,255,255,255)')))

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=list(X), y=list(y), name='Random 1', mode='lines'))
    fig2.update_layout(
        xaxis=dict(range=[X[0], X[-1]]),
        yaxis=dict(range=[min(y) - 0.1, max(y) + 0.1]),
        height=385)

    if value==False:
        time_interval = 9999999999999900000
        if last < 15 : 
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
            print(x[-1],x[-1])
            fig = go.Figure(
                data =  [candle,scatter]
            )
            return (string1,fig)
                   #  {'data': [candle,scatter],
                   #  'layout' : go.Layout(xaxis_rangeslider_visible=True,
                   #                      xaxis = dict(
                   #                      autorange=False,
                   #                      range = [x[0] , x[-1] ],
                   #                      type='date'),
                   #                      yaxis = dict(range = [min(low),max(high)]),
                   #  )}
                   # )
        else : 
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
            print(x[-1],x[-1])
            fig = go.Figure(
                data =  [candle,scatter]
            )
            return (string1,fig)
                   #  {'data': [candle,scatter],
                   #  'layout' : go.Layout(xaxis_rangeslider_visible=True,
                   #                      xaxis = dict(
                   #                      autorange=False,
                   #                      range = [x[-15] , x[-1] ],
                   #                      type='date'),
                   #                      yaxis = dict(range = [min(low),max(high)]),
                   #  )}
                   # )
    else:
        time_interval = 1500
        if last < len(df) : 
                if last < 15 : 
                    x.append(df.iloc[last,0])
                    open.append(df.iloc[last,4])
                    high.append(df.iloc[last,2])
                    low.append(df.iloc[last,3])
                    close.append(df.iloc[last,1])
            
                    candle = plotly.graph_objs.Candlestick(x = list(x),
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
                    print(x[0] ,x[-1])
                    return (string2, 
                            {'data': [candle,scatter],
                            'layout' : go.Layout(xaxis_rangeslider_visible=True,
                                                xaxis = dict(
                                                    autorange=False,
                                                    range = [x[0] , x[-1] ],
                                                    type='date'),
                                                yaxis = dict(range = [min(low),max(high)]),
                                                )} 
                            )
                else : 
                    x.append(df.iloc[last,0])
                    open.append(df.iloc[last,4])
                    high.append(df.iloc[last,2])
                    low.append(df.iloc[last,3])
                    close.append(df.iloc[last,1])
            
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
                    print(x[-15],x[-1])
                    return (string2,
                            {'data': [candle,scatter],
                            'layout' : go.Layout(xaxis_rangeslider_visible=True,
                                                xaxis = dict(
                                                    autorange=False,
                                                    range = [x[-15] , x[-1] ],
                                                    type='date'),
                                                yaxis = dict(range = [min(low),max(high)]),
                                                ) }
                           )
        else : 
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
            print(x[-15],x[-1])
            return (string2,{'data': [candle,scatter],
                    'layout' : go.Layout(xaxis_rangeslider_visible=True,
                                xaxis = dict(autorange=False,
                                            range = [x[-15] , x[-1] ],
                                            type='date'),
                                            yaxis = dict(range = [min(low),max(high)]),
                    )}
            )
        #return (string2,fig2)


if __name__ == '__main__':
    app.run_server(debug=True)


# df = pd.read_csv('working.csv')

# #x = deque(maxlen = 20)
# x = []
# x.append(df.iloc[0,0])

# #open = deque(maxlen = 20)
# open = []
# open.append(df.iloc[0,4])

# #high = deque(maxlen = 20)
# high = []
# high.append(df.iloc[0,2])

# #low = deque(maxlen = 20)
# low = []
# low.append(df.iloc[0,3])

# #close = deque(maxlen = 20)
# close = []
# close.append(df.iloc[0,1])

# #X = deque(maxlen = 20)
# X = []
# X.append(1)

# #Y = deque(maxlen = 20)
# Y = []
# Y.append(1)

# last = 0

# graph_update_disabled = False

# app = dash.Dash(__name__)
# server = app.server

# app.layout = html.Div(
#     [
#         daq.ToggleSwitch(
#             id='my-toggle-switch',
#             value=False
#         ),
#         html.Div(id='toggle-switch-output'),
        
#         dcc.Graph(id = 'live-graph', animate = False),
#         dcc.Interval(
#             id = 'graph-update',
#             interval = 2500,
#             n_intervals = 0,
#         ),
#     ]
# )
# @app.callback(
#     [Output('toggle-switch-output', 'children'),
#     Output('live-graph', 'figure'), ]
#     [Input('my-toggle-switch', 'value'),
#     Input('graph-update', 'n_intervals'),]
#     # [ Input('btn-nclicks-3', 'n_clicks') ] 
# )

# def update_graph_scatter(value,n):
#     global last
#     #return f'The stop button has been clicked '
    

#     # if len(X1) >= 100:
#     #     graph_updates_disabled = True
#     # if click is not None:
#     #     #my code here
#     #     # button is clicked
#     #     func = request.environ.get('werkzeug.server.shutdown')
#     #     if func is None:
#     #         raise RuntimeError('Not running with the Werkzeug Server')
#     #     func()
#     # else:
#     if value == False :
#             if last < len(df) : 
#                 if last < 15 : 
#                     x.append(df.iloc[last,0])
#                     open.append(df.iloc[last,4])
#                     high.append(df.iloc[last,2])
#                     low.append(df.iloc[last,3])
#                     close.append(df.iloc[last,1])
            
#                     candle = plotly.graph_objs.Candlestick(x = list(x),
#                             low = list(low),
#                             high = list(high),
#                             close = list(close),
#                             open = list(open),
#                             increasing_line_color = 'green',
#                             decreasing_line_color = 'red'
#                     )
#                     scatter = plotly.graph_objs.Scatter(
#                         x=list(x),
#                         y=list(open),
#                         name='Scatter',
#                         mode= 'lines+markers'
#                     )
#                     last = last + 1
#                     print(x[0] ,x[-1])
#                     return {'data': [candle,scatter],
#                             'layout' : go.Layout(xaxis_rangeslider_visible=True,
#                                                 xaxis = dict(
#                                                     autorange=False,
#                                                     range = [x[0] , x[-1] ],
#                                                     type='date'),
#                                                 yaxis = dict(range = [min(low),max(high)]),
#                                                 )}
#                 else : 
#                     x.append(df.iloc[last,0])
#                     open.append(df.iloc[last,4])
#                     high.append(df.iloc[last,2])
#                     low.append(df.iloc[last,3])
#                     close.append(df.iloc[last,1])
            
#                     candle = plotly.graph_objs.Candlestick(
#                             x = list(x),
#                             low = list(low),
#                             high = list(high),
#                             close = list(close),
#                             open = list(open),
#                             increasing_line_color = 'green',
#                             decreasing_line_color = 'red'
#                     )
#                     scatter = plotly.graph_objs.Scatter(
#                         x=list(x),
#                         y=list(open),
#                         name='Scatter',
#                         mode= 'lines+markers'
#                     )
#                     last = last + 1
#                     print(x[-15],x[-1])
#                     return {'data': [candle,scatter],
#                             'layout' : go.Layout(xaxis_rangeslider_visible=True,
#                                                 xaxis = dict(
#                                                     autorange=False,
#                                                     range = [x[-15] , x[-1] ],
#                                                     type='date'),
#                                                 yaxis = dict(range = [min(low),max(high)]),
#                                                 )}
#             else : 
#                 candle = plotly.graph_objs.Candlestick(
#                             x = list(x),
#                             low = list(low),
#                             high = list(high),
#                             close = list(close),
#                             open = list(open),
#                             increasing_line_color = 'green',
#                             decreasing_line_color = 'red'
#                 )
#                 scatter = plotly.graph_objs.Scatter(
#                     x=list(x),
#                     y=list(open),
#                     name='Scatter',
#                     mode= 'lines+markers'
#                 )
#                 print(x[-15],x[-1])
#                 return {'data': [candle,scatter],
#                         'layout' : go.Layout(xaxis_rangeslider_visible=True,
#                                 xaxis = dict(autorange=False,
#                                             range = [x[-15] , x[-1] ],
#                                             type='date'),
#                                             yaxis = dict(range = [min(low),max(high)]),
#                         )}
#     else :         
#         candle = plotly.graph_objs.Candlestick(
#                 x = list(x),
#                 low = list(low),
#                 high = list(high),
#                 close = list(close),
#                 open = list(open),
#                 increasing_line_color = 'green',
#                 decreasing_line_color = 'red'
#         )
#         scatter = plotly.graph_objs.Scatter(
#             x=list(x),
#             y=list(open),
#             name='Scatter',
#             mode= 'lines+markers'
#         )
#         print(x[-15],x[-1])
#         return {'data': [candle,scatter],
#                 'layout' : go.Layout(xaxis_rangeslider_visible=True,
#                                     xaxis = dict(
#                                     autorange=False,
#                                     range = [x[-15] , x[-1] ],
#                                     type='date'),
#                                     yaxis = dict(range = [min(low),max(high)]),
#         )}
        
#                 # func = request.environ.get('werkzeug.server.shutdown')
#                 # if func is None:
#                 #     raise RuntimeError('Not running with the Werkzeug Server')
#                 # func()

# if __name__ == '__main__':
#     app.run_server(debug=False)
