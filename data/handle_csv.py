#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   uyplayer
@License :   (C) Copyright 2013-2021, uyplayer.com
@Contact :   {uyplayer@qq.com}
@Software:   PyCharm
@File    :   handle_csv.py
@Time    :   2021/5/6 12:02 PM
@Desc    :
'''

import json
import pandas as pd
import datetime
import time

#data convert
def timetraptodate(t):
     # return datetime.datetime.strptime(t, "%Y-%m-%d")
     return time.strftime("%Y-%m-%d", time.localtime(t))

def json_csv():
    file_name = "../data/correlated assets/market_dominance_data.json"
    with open(file_name) as f:
        pop_data = json.load(f)
        btc_d = pd.DataFrame(pop_data['series_data_array'][0]['data'])
        btc_d.columns = ['Date', 'market_dominance']
        btc_d['Date'] = btc_d['Date'].apply(lambda x:timetraptodate(x//1000))
        # btc_d.index = btc_d.index.strftime('%Y-%m-%d')
        btc_d=btc_d.set_index('Date')
        print(btc_d)
        btc_d.to_csv("../data/correlated assets/market_dominance_data.csv")

json_csv()
