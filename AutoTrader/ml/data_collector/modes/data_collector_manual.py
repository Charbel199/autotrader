from AutoTrader.ml.data_collector.features_generator.features_generator import get_features_generator
from AutoTrader.data.previous_data.data_fetcher import get_fetcher
import pandas as pd
from AutoTrader.data.data_structures.structure import get_data_structure
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from AutoTrader.helper import date_helper, logger
from AutoTrader.ml.data_collector.generator.candlestick_generator import get_candlestick_generator
from plotly.graph_objs import Figure
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

log = logger.get_logger(__name__)


class DataCollectorManual(object):

    def __init__(self,
                 symbols: list,
                 timeframe: str,
                 data_fetcher_provider: str,
                 data_structure_provider: str,
                 features_generator_provider: str,
                 candlestick_generator_processor_provider: str,
                 start_date: str):
        self.data = {}
        self.fig = make_subplots(rows=1, cols=1)
        self.clicked_candlesticks = []
        self.start_date = start_date
        data_fetcher = get_fetcher(data_fetcher_provider)
        data_structure = get_data_structure(data_structure_provider)
        features_generator = get_features_generator(features_generator_provider, data_structure)
        self.generator = get_candlestick_generator(candlestick_generator_processor_provider, features_generator, data_fetcher, data_structure, symbols, timeframe)
        self.generator.fetch_new_candlesticks(date_helper.get_random_timestamp(date_helper.from_binance_date_to_timestamp(start_date)), 8)

    def get_new_candlesticks(self) -> None:
        # Save old data
        if len(self.clicked_candlesticks) > 0:
            print('candlesticks ', self.clicked_candlesticks)
            # print(self.data['ADX'].to_string())

        self.clicked_candlesticks = []
        self.data = self.generator.get_new_candlesticks()
        candlesticks = self.data['Ticks']
        df = pd.DataFrame(candlesticks)
        self.fig = make_subplots(rows=1, cols=1)
        self.fig.append_trace(go.Candlestick(x=df['Time'],
                                             open=df['Open'],
                                             high=df['High'],
                                             low=df['Low'],
                                             close=df['Close'], name="Candlesticks"), row=1, col=1)
        self.fig.update_layout(xaxis_rangeslider_visible=False)
        self.generator.fetch_new_candlesticks(date_helper.get_random_timestamp(date_helper.from_binance_date_to_timestamp(self.start_date)), 8)

    def click_candlestick(self, click: dict) -> None:
        if len(self.clicked_candlesticks) < 2:
            log.info(f"Candlestick clicked {click}")
            time = click['x']
            close = click['close']
            self.clicked_candlesticks.append({
                'Time': time,
                'Close': close
            })
            if len(self.clicked_candlesticks) == 1:
                self.fig.append_trace(go.Scatter(
                    x=[time],
                    y=[close],
                    marker=dict(color="gold", size=13, symbol=46),
                    mode="markers",
                    name="Buy"
                ), row=1, col=1)
            elif len(self.clicked_candlesticks) == 2:
                self.fig.append_trace(go.Scatter(
                    x=[time],
                    y=[close],
                    marker=dict(color="silver", size=13, symbol=45),
                    mode="markers",
                    name="Sell"), row=1, col=1)

    def get_fig(self) -> Figure:
        return self.fig

    def launch_manual_collector(self) -> None:
        self.get_new_candlesticks()
        fig = self.get_fig()
        app = dash.Dash()
        app.layout = html.Div([
            dcc.Graph(id='graph', figure=fig),
            dcc.Interval(
                id='graph-update',
                interval=1000
            ),
            html.Pre(id='click-data', style={'display': 'none'}),
            html.Button('Get new data', id='retrieve-data-button', n_clicks=0),
            html.Div(id='retrieve-data-output', style={'display': 'none'}),

        ])

        @app.callback(
            Output('click-data', 'children'),
            [Input('graph', 'clickData')])
        def display_click_data(click_data):
            if click_data is not None:
                self.click_candlestick(click_data['points'][0])

        @app.callback(
            Output(component_id='graph', component_property='figure'),
            [Input(component_id='graph-update', component_property='n_intervals')]
        )
        def update_graph(_):
            return self.get_fig()

        @app.callback(
            Output(component_id='retrieve-data-output', component_property='children'),
            [Input(component_id='retrieve-data-button', component_property='n_clicks')])
        def retrieve_data(n_clicks):
            if n_clicks <= 0:
                return
            log.info('Getting new candlesticks')
            self.get_new_candlesticks()
            return

        app.run_server(debug=True, use_reloader=False)
