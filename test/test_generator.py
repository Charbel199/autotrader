from dotenv import load_dotenv
from data.data_logger import logger

load_dotenv()
log = logger.setup_applevel_logger(file_name='test_generator_debug.log')
from ml.candlestick_generator import CandlestickGeneratorRunner
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

start_date = "1 Oct, 2018"

runner = CandlestickGeneratorRunner(symbols=['DOGEUSDT', 'BTCUSDT', 'ADAUSDT'], timeframe='5m', data_fetcher_provider='binance',
                                    data_structure_provider='pandas', candlestick_processor_provider='simple', start_date=start_date)
runner.get_new_candlesticks()
fig = runner.get_fig()
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
        runner.click_candlestick(click_data['points'][0])


@app.callback(
    Output(component_id='graph', component_property='figure'),
    [Input(component_id='graph-update', component_property='n_intervals')]
)
def update_graph(_):
    return runner.get_fig()


@app.callback(
    Output(component_id='retrieve-data-output', component_property='children'),
    [Input(component_id='retrieve-data-button', component_property='n_clicks')])
def retrieve_data(n_clicks):
    if n_clicks <= 0:
        return
    log.info('Getting new candlesticks')
    runner.get_new_candlesticks()
    return


app.run_server(debug=True, use_reloader=False)
