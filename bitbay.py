import requests
import json
from datetime import datetime
from requests import session
from requests.api import request
from requests.sessions import Session

from pprint import pprint as pp

marketCode = 'BTC-USD'

interval = {    '1min': 60,
                '15min': 900,
                '1h': 3600,
                '1d': 86400,
                '1w': 604800
            }


time_from = 1002042800000
time_to = 1632042800000


def date_to_sec(date):
    current_timestamp = date.timestamp() * 1000
    current_timestamp = str(current_timestamp)[0:13]
    print(current_timestamp)
    return current_timestamp

def sec_to_date(timestamp):
    current_date = datetime.fromtimestamp(int(str(timestamp)[0:10]))
    print(current_date)
    return current_date

class BitBay:
    def __init__(self):
        self.apiurl = "https://api.bitbay.net/rest"
        self.headers = {'content-type': 'application/json'}
        self.session = Session()
        self.session.headers.update(self.headers)

    def getMarket(self, marketCode):
        url = self.apiurl + f'/trading/ticker/{marketCode}'
        response = self.session.get(url)
        data_text = json.loads(response.text)

        pp(data_text)
        print(sec_to_date(data_text.get('ticker').get('time')))

    def getMarketHistory(self, market_code, interval_key, date_from, date_to):
        url = self.apiurl + f'/trading/candle/history/{market_code}/{interval[interval_key]}'
        querystring = {"from": date_from, "to": date_to}
        response = self.session.get(url, params=querystring)
        data_text = json.loads(response.text)

        for el in data_text['items']:
            print(sec_to_date(el[0]))
            print(el[1])

resp = BitBay()
resp.getMarket('btc-usd')
# resp.getMarketHistory('btc-usd', '1d', time_from, time_to)

