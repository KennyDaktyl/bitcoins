from os import close
import requests
import json
from datetime import datetime
from requests import session
from requests.api import request
from requests.sessions import Session

from pprint import pprint as pp
import pendulum

now = pendulum.now("Europe/Warsaw")

time_start = pendulum.datetime(2014, 5, 12, tz="Europe/Warsaw")
# print(time_start.to_iso8601_string())
# print(now.int_timestamp)

print(datetime.fromtimestamp(1630972800))

marketCode = 'BTC-USD'

interval = {    '1min': 60,
                '15min': 900,
                '1h': 3600,
                '1d': 86400,
                '1w': 604800
            }


time_from = time_start.int_timestamp * 1000
time_to = 1632042800000

file1 = open("table_per_day.txt","w")


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
        file1 = open("table_per_day.txt","w")
        for el in data_text['items']:
            print(10000000000 / 1000) 
            print(el[1])
            file1.write(str(int(int(el[0]) / 1000)) + "\t" + str(round(float(el[1]['o']), 2)) + "\n")
        file1.close()



resp = BitBay()
# resp.getMarket('btc-usd')
resp.getMarketHistory('btc-usd', '1min', time_from, time_to)

