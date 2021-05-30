#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   uyplayer
@License :   (C) Copyright 2013-2021, uyplayer.com
@Contact :   {uyplayer@qq.com}
@Software:   PyCharm
@File    :   DEMA.py
@Time    :   2021/4/23 11:32 PM
@Desc    :   DEMA - Double Exponential Moving Average

'''

'''
https://www.investopedia.com/terms/d/double-exponential-moving-average.asp
https://www.investopedia.com/ask/answers/121814/what-double-exponential-moving-average-dema-formula-and-how-it-calculated.asp
'''

import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from talib import DEMA

api_key = 'b343286b81c604c7ba852765a9cbf9ac'
stock = 'aapl'

stockprices = requests.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?serietype=line&apikey={api_key}")
stockprices = stockprices.json()

# Parse the response and select only last 150 days of prices
stockprices = stockprices['historical'][-150:]

stockprices = pd.DataFrame.from_dict(stockprices)
stockprices = stockprices.set_index('date')

real = DEMA(stockprices['close'], timeperiod=30)

df = pd.DataFrame()

df['close'] = stockprices['close']
df['dema'] = real


print(df)

ax = df[['close','dema']].plot(figsize=(10, 4))
plt.title(stock + ' DEMA')
plt.axis('tight')
plt.ylabel('Price')
plt.savefig('apple.png', bbox_inches='tight')
plt.show()

