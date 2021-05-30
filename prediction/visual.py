#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   uyplayer
@License :   (C) Copyright 2013-2021, uyplayer.com
@Contact :   {uyplayer@qq.com}
@Software:   PyCharm
@File    :   visual.py
@Time    :   2021/5/10 7:44 PM
@Desc    :   visualize
'''

import pandas as pd
import datetime
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
from prediction.utils import btc_data,get_technical_indicators



def plot_btc_csv(btc_df):
    print(btc_df)
    y_height = max(btc_df['Close'])
    plt.figure(figsize=(14, 5))
    plt.plot(btc_df['Date'], btc_df['Close'], label='Bitcoin Close proce')
    plt.vlines(datetime.date(2021, 4, 1), 0, y_height, linestyles='--', colors='gray', label='Train/Test data cut-off')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Bitcoin price')
    plt.legend()
    plt.show()


# plot_technical_indicators
def plot_technical_indicators(dataset, last_days):
    plt.figure(figsize=(16, 12), dpi=100)
    shape_0 = dataset.shape[0]
    xmacd_ = shape_0 - last_days

    dataset = dataset.iloc[-last_days:, :]
    x_ = range(3, dataset.shape[0])
    x_ = list(dataset.index)
    #     print(x_)
    # Plot first subplot
    plt.subplot(2, 1, 1)
    plt.plot(dataset['ma7'], label='MA 7', color='g', linestyle='--')
    plt.plot(dataset['Close'], label='Closing Price', color='b')
    plt.plot(dataset['ma21'], label='MA 21', color='r', linestyle='--')
    plt.plot(dataset['upper_band'], label='Upper Band', color='c')
    plt.plot(dataset['lower_band'], label='Lower Band', color='c')
    plt.fill_between(x_, dataset['lower_band'], dataset['upper_band'], alpha=0.35)
    plt.title('Technical indicators for  Bitcoin - last {} days.'.format(last_days))
    plt.ylabel('USD')
    plt.legend()

    # Plot second subplot
    # print(xmacd_)
    plt.subplot(2, 1, 2)
    plt.title('MACD')
    plt.plot(dataset['MACD'], label='MACD', linestyle='-.')
    plt.hlines(max(dataset['MACD']), xmacd_, shape_0, colors='g', linestyles='--')
    plt.hlines(min(dataset['MACD']), xmacd_, shape_0, colors='g', linestyles='--')
    plt.plot(dataset['log_momentum'], label='Momentum', color='b', linestyle='-')

    plt.legend()
    plt.show()

    # Plot second subplot
    plt.subplot(2, 1, 2)
    plt.title('MACD')
    plt.plot(dataset['MACD'], label='MACD', linestyle='-.')
    plt.hlines(15, xmacd_, shape_0, colors='g', linestyles='--')
    plt.hlines(-15, xmacd_, shape_0, colors='g', linestyles='--')
    plt.plot(dataset['log_momentum'], label='Momentum', color='b', linestyle='-')

    plt.legend()
    plt.show()

if __name__=='__main__':
    data = btc_data()
    data_tc = get_technical_indicators(data)
    plot_technical_indicators(data_tc, 400)
