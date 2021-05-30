#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   uyplayer
@License :   (C) Copyright 2013-2021, uyplayer.com
@Contact :   {uyplayer@qq.com}
@Software:   PyCharm
@File    :   mama.py
@Time    :   2021/4/24 4:03 PM
@Desc    :   MAVP - Moving average with variable period
'''

import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from talib import MAVP


api_key = 'b343286b81c604c7ba852765a9cbf9ac'
stock = 'aapl'

stockprices = requests.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?serietype=line&apikey={api_key}")
stockprices = stockprices.json()

# Parse the response and select only last 150 days of prices
stockprices = stockprices['historical'][-300:]

stockprices = pd.DataFrame.from_dict(stockprices)
stockprices = stockprices.set_index('date')

real = MAVP(stockprices['close'],20, minperiod=2, maxperiod=30, matype=0)

df = pd.DataFrame()

df['close'] = stockprices['close']
df['mavp'] = real

print(df)

ax = df[['close','mavp']].plot(figsize=(10, 4))
plt.title(stock + ' Moving average with variable period')
plt.axis('tight')
plt.ylabel('Price')
plt.savefig('apple.png', bbox_inches='tight')
plt.show()
