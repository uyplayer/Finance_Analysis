#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   uyplayer
@License :   (C) Copyright 2013-2021, uyplayer.com
@Contact :   {uyplayer@qq.com}
@Software:   PyCharm
@File    :   backtest1.py
@Time    :   2021/4/15 10:09 AM
@Desc    :
'''

# Library
# zipline
import zipline
from zipline import run_algorithm
from zipline.api import order_target_percent, symbol,set_benchmark
# data
from datetime import datetime
import pytz
# visualization
import matplotlib.pyplot as plt
import pandas as pd



# init
def initialize(context):
    # Which stock to trade
    context.stock = symbol('AAPL')
    context.index_average_window = 100
    # set_benchmark(False)
    zipline.api.set_benchmark(symbol('AAPL'))


# handle data
def handle_data(context, data):
    # get data
    equities_hist = data.history(context.stock, 'close', context.index_average_window, '1d')

    # 查看股票趋势，如果股价未来会涨，我们做多
    if equities_hist[-1] > equities_hist.mean():
        stock_weight = 1.0 # 做多
    else:
        stock_weight = 0.0 # 持平

    # 下单
    order_target_percent(context.stock, stock_weight)


def analyze(context, perf):
    fig = plt.figure()

    # 总资产
    ax = fig.add_subplot(311)
    ax.set_title('Strategy Results')
    ax.semilogy(perf['portfolio_value'], linestyle='-',
                label='Equity Curve', linewidth=3.0)
    ax.legend()
    ax.grid(False)

    # 总杠杆
    ax = fig.add_subplot(312)
    ax.plot(perf['gross_leverage'],
            label='Exposure', linestyle='-', linewidth=1.0)
    ax.legend()
    ax.grid(True)

    # 回报
    ax = fig.add_subplot(313)
    ax.plot(perf['returns'], label='Returns', linestyle='-.', linewidth=1.0)
    ax.legend()
    ax.grid(True)

    plt.show()


# 确定时间
start_date = pd.to_datetime('1999-11-18', utc=True)
end_date = pd.to_datetime('2018-03-17', utc=True)

# 回测
results = run_algorithm(
    start=start_date,
    end=end_date,
    initialize=initialize,
    analyze=analyze,
    handle_data=handle_data,
    capital_base=10000,
    data_frequency = 'daily', bundle='quandl'
)

