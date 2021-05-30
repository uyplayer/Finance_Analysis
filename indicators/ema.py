#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   uyplayer
@License :   (C) Copyright 2013-2021, uyplayer.com
@Contact :   {uyplayer@qq.com}
@Software:   PyCharm
@File    :   ema.py
@Time    :   2021/4/23 11:38 PM
@Desc    :   EMA - Exponential Moving Average
'''

"""
https://www.investopedia.com/ask/answers/122314/what-exponential-moving-average-ema-formula-and-how-ema-calculated.asp
https://www.investopedia.com/terms/e/ema.asp
"""

import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from talib import EMA


api_key = 'b343286b81c604c7ba852765a9cbf9ac'
stock = 'aapl'

stockprices = requests.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?serietype=line&apikey={api_key}")
stockprices = stockprices.json()

# Parse the response and select only last 150 days of prices
stockprices = stockprices['historical'][-150:]

stockprices = pd.DataFrame.from_dict(stockprices)
stockprices = stockprices.set_index('date')

real = EMA(stockprices['close'], timeperiod=30)

df = pd.DataFrame()

df['close'] = stockprices['close']
df['ema'] = real

print(df)

ax = df[['close','ema']].plot(figsize=(10, 4))
plt.title(stock + ' Exponential Moving Average')
plt.axis('tight')
plt.ylabel('Price')
plt.savefig('apple.png', bbox_inches='tight')
plt.show()

