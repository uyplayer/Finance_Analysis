#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   uyplayer
@License :   (C) Copyright 2013-2021, uyplayer.com
@Contact :   {uyplayer@qq.com}
@Software:   PyCharm
@File    :   Hilbert Transform.py
@Time    :   2021/4/24 10:40 AM
@Desc    :  HT_TRENDLINE - Hilbert Transform
'''

import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from talib import HT_TRENDLINE

api_key = 'b343286b81c604c7ba852765a9cbf9ac'
stock = 'aapl'

stockprices = requests.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?serietype=line&apikey={api_key}")
stockprices = stockprices.json()

# Parse the response and select only last 150 days of prices
stockprices = stockprices['historical'][-150:]

stockprices = pd.DataFrame.from_dict(stockprices)
stockprices = stockprices.set_index('date')

real = HT_TRENDLINE(stockprices['close'])

df = pd.DataFrame()

df['close'] = stockprices['close']
df['ht'] = real

print(df)

ax = df[['close','ht']].plot(figsize=(10, 4))
plt.title(stock + ' HT_TRENDLINE')
plt.axis('tight')
plt.ylabel('Price')
plt.savefig('apple.png', bbox_inches='tight')
plt.show()