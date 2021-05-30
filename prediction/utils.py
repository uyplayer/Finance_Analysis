
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   uyplayer
@License :   (C) Copyright 2013-2021, uyplayer.com
@Contact :   {uyplayer@qq.com}
@Software:   PyCharm
@File    :   utils.py
@Time    :   2021/5/10 7:34 PM
@Desc    :   utils for prebtc
'''

import datetime
import pandas as pd
import numpy as np


# date convert
def parser(x):
    return datetime.datetime.strptime(x,'%Y-%m-%d')


# generate indicators
def get_technical_indicators(dataset):
    # Create 7 and 21 days Moving Average
    dataset['ma7'] = dataset['Close'].rolling(window=7).mean()
    dataset['ma21'] = dataset['Close'].rolling(window=21).mean()

    # Create MACD
    dataset['26ema'] = pd.ewma(dataset['Close'], span=26)
    dataset['12ema'] = pd.ewma(dataset['Close'], span=12)
    dataset['MACD'] = (dataset['12ema'] - dataset['26ema'])

    # Create Bollinger Bands
    dataset['20sd'] = pd.stats.moments.rolling_std(dataset['Close'], 20)
    dataset['upper_band'] = dataset['ma21'] + (dataset['20sd'] * 2)
    dataset['lower_band'] = dataset['ma21'] - (dataset['20sd'] * 2)

    # Create Exponential moving average
    dataset['ema'] = dataset['Close'].ewm(com=0.5).mean()

    # Create Momentum
    dataset['momentum'] = dataset['Close'] - 1
    dataset['log_momentum'] = dataset['momentum'].apply(np.log)

    return dataset

# load data
# load datra
def btc_data():
    btc_df= pd.read_csv('../data/BTC-USD.csv', header=0, parse_dates=[0], date_parser=parser)
    # btc_df=btc_df.set_index('Date')
    # btc_df = btc_df[(btc_df['Date'] > '2014-09-17') & (btc_df['Date'] <= '2021-05-05')]
    return btc_df

