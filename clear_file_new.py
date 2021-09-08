import os
import json
from datetime import datetime
from requests import session
from requests.api import request
from requests.sessions import Session

import pendulum
from pprint import pprint as pp


file_name = 'table_per_day_new.txt'
market_code = 'BTC-USD'
interval = {    '1min': 60,
                '15min': 900,
                '1h': 3600,
                '1d': 86400,
                '1w': 604800
            }
interval_set = interval['1min']
seconds_range = 3600

today = datetime.now()

def set_new_time_range(timestamp, seconds_range):
    timestamp_end = int(timestamp) // 1000
    timestamp_end = timestamp_end + seconds_range
    timestamp_end = timestamp_end * 1000
    return timestamp_end

# first bitcoin
datetime_start = pendulum.datetime(2014, 5, 12, tz="Europe/Warsaw")
timestamp_from = int(datetime_start.int_timestamp) * 1000
timestamp_end = set_new_time_range(timestamp_from, seconds_range)

# finish while
timestamp_finish = pendulum.datetime(today.year, today.month, today.day, tz="Europe/Warsaw")
timestamp_finish = int(timestamp_finish.int_timestamp) * 1000

class BitBay:
    def __init__(self):
        self.apiurl = "https://api.bitbay.net/rest"
        self.headers = {'content-type': 'application/json'}
        self.session = Session()
        self.session.headers.update(self.headers)

    def getMarketHistory(self, market_code, interval_set, date_from, date_end, file_name):
        url = self.apiurl + f'/trading/candle/history/{market_code}/{interval_set}'
        querystring = {"from": date_from, "to": date_end}
        response = self.session.get(url, params=querystring)
        data_text = json.loads(response.text)
        print(data_text)
        if data_text.get('items'):
            with open(file_name, 'a') as f:
                for el in data_text['items']:
                    f.write(str(el[0]) + "\t" + "%.2f" % float(el[1]['o']) + "\n")
            return True
        else:
            return False

def read_write_file(timestamp_from):
    with open(file_name) as f:
        if os.stat(file_name).st_size == 0:
            timestamp_end = timestamp_from
        else:
            lines = f.read().splitlines()
            last_line = lines[-1].split("\t")
            timestamp_from = set_new_time_range(last_line[0], seconds_range)
            timestamp_end = set_new_time_range(timestamp_from, seconds_range)
        return (timestamp_from, timestamp_end)

resp = BitBay()
timestamp_from, timestamp_end = read_write_file(timestamp_from)

while timestamp_end < timestamp_finish:
    
    print("Nowe dane: " + str(timestamp_from) + ", " + str(timestamp_end))
    if resp.getMarketHistory(market_code, interval_set, timestamp_from, timestamp_end, file_name):
        timestamp_from, timestamp_end = read_write_file(timestamp_from)
    else:
        timestamp_from = timestamp_end
        timestamp_end = set_new_time_range(timestamp_from, seconds_range)
