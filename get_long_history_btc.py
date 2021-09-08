import os
import json
from datetime import datetime
from requests import session
from requests.api import request
from requests.sessions import Session

import pendulum
from pprint import pprint as pp


file_name = 'table_per_day.txt'
market_code = 'BTC-USD'
interval = {    '1min': 60,
                '15min': 900,
                '1h': 3600,
                '1d': 86400,
                '1w': 604800
            }
interval_set = interval['1min']
today = datetime.now()

# first bitcoin
time_start = pendulum.datetime(2014, 5, 12, tz="Europe/Warsaw")
time_from = int(time_start.int_timestamp) * 1000

file1 = open(file_name,"a")
if os.stat(file_name).st_size == 0:
    file1.write(str(time_from) + "\t" + "\n")
    time_end = time_from
else:
    with open(file_name) as f:
        lines = f.read().splitlines()
        last_line = lines[-1].split("\t")
        time_from = last_line[0]
file1.close()
time_end = int(int(time_from) / 1000)
time_end = int(int(time_end) + 3600)
time_end = int(time_end * 1000)


class BitBay:
    def __init__(self):
        self.apiurl = "https://api.bitbay.net/rest"
        self.headers = {'content-type': 'application/json'}
        self.session = Session()
        self.session.headers.update(self.headers)

    def getMarketHistory(self, market_code, interval_set, date_from, date_end):
        url = self.apiurl + f'/trading/candle/history/{market_code}/{interval_set}'
        querystring = {"from": date_from, "to": date_end}
        response = self.session.get(url, params=querystring)
        data_text = json.loads(response.text)
        print(data_text)
        file1 = open("table_per_day.txt","a")
        if data_text.get('items'):
            for el in data_text['items']:
                file1.write(str(int(int(el[0]))) + "\t" + "%.2f" % float(el[1]['o']) + "\n")
                file1.write(str(time_end) + "\n")
        else:
            file1.write(str(time_end) + "\t" + "\n")        
        file1.close()
    

print(time_from, time_end)
now = datetime.now()
time_finish = pendulum.datetime(today.year, today.month, today.day, tz="Europe/Warsaw")
time_finish = int(time_finish.int_timestamp) * 1000
print(time_finish)
resp = BitBay()

while time_end < time_finish:
    time_start = pendulum.datetime(2014, 5, 12, tz="Europe/Warsaw")
    time_from = int(time_start.int_timestamp) * 1000

    file1 = open(file_name,"a")
    if os.stat(file_name).st_size == 0:
        file1.write(str(time_from) + "\t" + "\n")
        time_end = time_from
    else:
        with open(file_name) as f:
            lines = f.read().splitlines()
            last_line = lines[-1].split("\t")
            time_from = last_line[0]
    file1.close()
    time_end = int(int(time_from) / 1000)
    time_end = int(int(time_end) + 3600)
    time_end = int(time_end * 1000)
    resp.getMarketHistory(market_code, interval_set, time_from, time_end)
