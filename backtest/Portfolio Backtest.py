#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   uyplayer
@License :   (C) Copyright 2013-2021, uyplayer.com
@Contact :   {uyplayer@qq.com}
@Software:   PyCharm
@File    :   Portfolio Backtest.py
@Time    :   2021/4/15 12:26 PM
@Desc    :
'''

# Library
# zipline
import zipline
from zipline import run_algorithm
from zipline.api import order_target_percent, symbol, set_benchmark
# data
from datetime import datetime
import pytz
# visualization
import matplotlib.pyplot as plt
import pandas as pd


def initialize(context):
    # 股票名单
    dji = [
        "AAPL",
        "AXP",
        "BA",
        "CAT",
        "CSCO",
        "CVX",
        "DIS",
        "DWDP",
        "GS",
        "HD",
        "IBM",
        "INTC",
        "JNJ",
        "JPM",
        "KO",
        "MCD",
        "MMM",
        "MRK",
        "MSFT",
        "NKE",
        "PFE",
        "PG",
        "TRV",
        "UNH",
        "UTX",
        "V",
        "VZ",
        "WBA",
        "WMT",
        "XOM",
    ]

    # 列所有的股票
    context.dji_symbols = [symbol(s) for s in dji]

    # 平均移动窗口大小
    context.index_average_window = 100


def handle_data(context, data):
    # 提取历史数据
    stock_hist = data.history(context.dji_symbols, "close", context.index_average_window, "1d")

    # 空出一个DataFrame，为了后期使用
    stock_analytics = pd.DataFrame()

    # 在平均价位上面，返货true 或者false
    stock_analytics['above_mean'] = stock_hist.iloc[-1] > stock_hist.mean()

    # 筛选True的股票，这就是我们想要购买的
    stock_analytics.loc[stock_analytics['above_mean'] == True, 'weight'] = 1 / len(context.dji_symbols)

    # 如果是false 就不买
    stock_analytics.loc[stock_analytics['above_mean'] == False, 'weight'] = 0.0

    # 循环开始
    for stock, analytics in stock_analytics.iterrows():
        # 查看可以交易的股票
        if data.can_trade(stock):
            # Place the trade
            order_target_percent(stock, analytics['weight'])


def analyze(context, perf):
    fig = plt.figure()

    # First chart
    ax = fig.add_subplot(311)
    ax.set_title('Strategy Results')
    ax.plot(perf['portfolio_value'], linestyle='-',
            label='Equity Curve', linewidth=3.0)
    ax.legend()
    ax.grid(False)

    # 总杠杆
    ax = fig.add_subplot(312)
    ax.plot(perf['gross_leverage'],
            label='Exposure', linestyle='-', linewidth=1.0)
    ax.legend()
    ax.grid(True)

    # Third chart
    ax = fig.add_subplot(313)
    ax.plot(perf['returns'], label='Returns', linestyle='-.', linewidth=1.0)
    ax.legend()
    ax.grid(True)

    plt.show()


# Set start and end date
start = datetime(2003, 1, 1, tzinfo=pytz.UTC)
end = datetime(2017, 12, 31, tzinfo=pytz.UTC)

# Fire off the backtest
results = run_algorithm(start=start, end=end,
                        initialize=initialize, analyze=analyze,
                        handle_data=handle_data,
                        capital_base=10000,
                        data_frequency='daily', bundle='quandl')