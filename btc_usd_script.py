from os import close
import json
from datetime import datetime
from requests import session
from requests.api import request
from requests.sessions import Session

import pendulum


file1 = open("table_per_day.txt","w")
market_code = 'BTC-USD'
interval = {    '1min': 60,
                '15min': 900,
                '1h': 3600,
                '1d': 86400,
                '1w': 604800
            }
interval_set = interval['1d']
today = datetime.now()

# first bitcoin
time_start = pendulum.datetime(2014, 5, 12, tz="Europe/Warsaw")
time_now = pendulum.datetime(today.year, today.month, today.day, tz="Europe/Warsaw")

time_from = time_start.int_timestamp * 1000
time_to = time_now.int_timestamp * 1000


class BitBay:
    def __init__(self):
        self.apiurl = "https://api.bitbay.net/rest"
        self.headers = {'content-type': 'application/json'}
        self.session = Session()
        self.session.headers.update(self.headers)

    def getMarketHistory(self, market_code, interval_set, date_from, date_to):
        url = self.apiurl + f'/trading/candle/history/{market_code}/{interval_set}'
        querystring = {"from": date_from, "to": date_to}
        response = self.session.get(url, params=querystring)
        data_text = json.loads(response.text)
        file1 = open("table_per_day.txt","w")
        for el in data_text['items']:
            file1.write(str(int(int(el[0]) / 1000)) + "\t" + "%.2f" % float(el[1]['o']) + "\n")
        file1.close()



resp = BitBay()
resp.getMarketHistory(market_code, interval_set, time_from, time_to)

