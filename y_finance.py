import numpy as np
import pandas as pd
# from pandas._libs.tslibs import Hour

#Data Source
import yfinance as yf

#Data viz
import plotly.graph_objs as go
from yfinance import tickers

data = yf.download(tickers="BTC-USD", period='60d', interval='15m')

print(data)

fig = go.Figure()
fig.add_trace(go.Candlestick(x=data.index,
                             open=data['Open'],
                             high=data['High'],
                             low=data['Low'],
                             close=data['Close'],
                             name="Market data"
                                )
)

fig.update_layout(
    title="BitCoins Layout",
    yaxis_title="Stock prices (per USD)"
)

fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=15, label='15min', step='minute', stepmode='backward'),
            dict(count=45, label='45min', step='minute', stepmode='backward'),
            dict(count=1, label='HTD', step='hour', stepmode='todate'),
            dict(count=6, label='6h', step='hour', stepmode='backward'),
            dict(step='all')
        ])
    )
)

fig.show()