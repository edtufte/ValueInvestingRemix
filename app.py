# TODO: 
# - Add in financial metrics / income statement information to dataframe
# - Add in value investing logic warning flags
# - Add in calculation for current stock price value
# - Conditional formatting on stock price chart - green pos / red negative
# - Add in trendline to stock price chart
# - Build out requirements.txt and readme.md

from fileinput import close
from operator import index
import dash
from dash.dependencies import Input, Output
from dash import dcc, html
import numpy as np
from pandas_datareader import data as web
from pandas_datareader import get_nasdaq_symbols
from datetime import datetime as dt

# create app
app = dash.Dash(__name__)
server = app.server

# create stock ticker dropdowns
# stocklist = []
nasdaqlist = get_nasdaq_symbols()

# default date options
begin_stock_range = dt(2012, 1, 1)
end_stock_range = dt.now()

app.layout = html.Div([
    html.Div([

        html.H1('Value Investing'),
        # First let users choose stocks
        html.H2('Choose a stock ticker'),
        dcc.Dropdown(
            id='ticker-dropdown',
            # options=['AMZN','KO'],
            options=nasdaqlist['NASDAQ Symbol'].tolist()
            # value='AMZN'
        ),
        html.H2('Stock Price Graph'),
        dcc.Graph(id='stock-graph'),
        html.P('')

    ],style={'width': '40%', 'display': 'inline-block'}),
    html.Div([
        html.H2('Critical Variables and Ratios'),
        html.Table(id='metrics-table'),
        html.P(''),
        html.H2('Warning Flags'),
        html.Table(id='reason-list'),
        html.P('')
    ], style={'width': '55%', 'float': 'right', 'display': 'inline-block'}),
    html.H4('Date Range for Stock Chart'),
    dcc.DatePickerRange(
        id='stock-date-range-picker',
        min_date_allowed=dt(1910, 8, 5),
        max_date_allowed=dt.now(),
        initial_visible_month=begin_stock_range,
        start_date=begin_stock_range,
        end_date=end_stock_range
    ),
    html.Table(id='stock-date-range')
])

@app.callback(
    Output('stock-graph', 'figure'),
    Input('ticker-dropdown', 'value'),
    Input('stock-date-range-picker', 'start_date'),
    Input('stock-date-range-picker', 'end_date'),
    prevent_initial_call=True
)
def update_stock_graph(selected_dropdown_value, start_date, end_date):
    global stockpricedf
    stockpricedf = web.DataReader(
        selected_dropdown_value.strip(), data_source='yahoo',
        start=start_date, end=end_date
    )
    return {
        'data': [{
            'x': stockpricedf.index,
            'y': stockpricedf.Close
        }]
    }



if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port="8050")