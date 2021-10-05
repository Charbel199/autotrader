import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.graph_objects as go # or plotly.express as px


import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

def show_candlesticks(df):
    fig = make_subplots(rows=3, cols=1)
    fig.append_trace(go.Candlestick(x=df['Time'],
                                    open=df['Open'],
                                    high=df['High'],
                                    low=df['Low'],
                                    close=df['Close'], name="Candlesticks"), row=1, col=1)


    app = dash.Dash()
    app.layout = html.Div([
        dcc.Graph(id='graph',figure=fig),
        html.Div([
            dcc.Markdown("""
                   **Click Data**

                   Click on markets in the graph.
               """),
            html.Pre(id='click-data'),
        ], className='three columns')
    ])
    @app.callback(
    Output('click-data', 'children'),
    [Input('graph', 'clickData')])
    def display_click_data(clickData):
        print(clickData)

    app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter
