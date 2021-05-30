#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   uyplayer
@License :   (C) Copyright 2013-2021, uyplayer.com
@Contact :   {uyplayer@qq.com}
@Software:   PyCharm
@File    :   bollinger_bands.py
@Time    :   2021/4/23 5:53 PM
@Desc    :   bollinger_bands
'''

# https://codingandfun.com/bollinger-bands-pyt

import requests
import pandas as pd
import matplotlib.pyplot as plt
from talib import BBANDS

api_key= 'b343286b81c604c7ba852765a9cbf9ac'

def bollingerbands(stock):
    stockprices = requests.get(f"https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?serietype=line&apikey={api_key}")
    stockprices = stockprices.json()

    # Parse the response and select only last 150 days of prices
    stockprices = stockprices['historical'][-150:]

    stockprices = pd.DataFrame.from_dict(stockprices)
    stockprices = stockprices.set_index('date')

    # 20 days moving Average
    stockprices['MA20'] = stockprices['close'].rolling(window=20).mean()
    # 20 days standard deviation
    stockprices['20dSTD'] = stockprices['close'].rolling(window=20).std()


    stockprices['Upper'] = stockprices['MA20'] + (stockprices['20dSTD'] * 2)

    stockprices['Lower'] = stockprices['MA20'] - (stockprices['20dSTD'] * 2)


    ax=stockprices[['close', 'MA20', 'Upper', 'Lower']].plot(figsize=(10, 4))
    ax.fill_between(stockprices.index, stockprices['Upper'], stockprices['Lower'], facecolor='orange', alpha=0.1)
    plt.title(stock + ' Bollinger Bands')
    plt.axis('tight')
    plt.ylabel('Price')
    plt.savefig('apple.png', bbox_inches='tight')
    plt.show()

def mytalib(stock):

    stockprices = requests.get(
        f"https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?serietype=line&apikey={api_key}")
    stockprices = stockprices.json()

    # Parse the response and select only last 150 days of prices
    stockprices = stockprices['historical'][-150:]

    stockprices = pd.DataFrame.from_dict(stockprices)
    stockprices = stockprices.set_index('date')

    upperband, middleband, lowerband = BBANDS(stockprices['close'], timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)

    df = pd.DataFrame()

    df['close'] = stockprices['close']
    df['upperband'] = upperband
    df['middleband'] = middleband
    df['lowerband'] = lowerband

    print(df)

    ax = df[['close','upperband', 'middleband', 'lowerband']].plot(figsize=(10, 4))
    ax.fill_between(df.index, df['upperband'], df['lowerband'], facecolor='orange', alpha=0.1)
    plt.title(stock + ' Bollinger Bands')
    plt.axis('tight')
    plt.ylabel('Price')
    plt.savefig('apple.png', bbox_inches='tight')
    plt.show()



# bollingerbands('aapl')

mytalib('aapl')