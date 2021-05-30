#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   uyplayer
@License :   (C) Copyright 2013-2021, uyplayer.com
@Contact :   {uyplayer@qq.com}
@Software:   PyCharm
@File    :   Backtest Analysis.py
@Time    :   2021/4/15 2:00 PM
@Desc    :
'''

# Library
# zipline
import pyfolio as pf
import zipline
from zipline import run_algorithm
from zipline.api import order_target_percent, symbol,set_benchmark,schedule_function
from zipline.utils.events import date_rules, time_rules
# data
from datetime import datetime
import pytz
# visualization
from matplotlib import pyplot as plt, rc, ticker
import pandas as pd
import numpy as np
import pandas as pd

# init
def initialize(context):
    # 要分析的股票
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

    # 循环上面的所有的股票
    context.universe = [symbol(s) for s in dji]
    # 平均移动窗口大小
    context.history_window = 20
    # 筛选我们要的股票的数量
    context.stocks_to_hold = 10
    # set_benchmark(False)
    zipline.api.set_benchmark(symbol('AAPL'))
    # 做一个计划：每月一次交易的
    schedule_function(handle_data, date_rules.month_start(), time_rules.market_close())



def month_perf(ts):
    perf = (ts[-1] / ts[0]) - 1
    return perf


def handle_data(context, data):
    # 提取数据
    hist = data.history(context.universe, "close", context.history_window, "1d")

    # 计算一个月的回报率并排序
    perf_table = hist.apply(month_perf).sort_values(ascending=False)

    # 提取前10个股票
    buy_list = perf_table[:context.stocks_to_hold]

    # 不在那10股票名单里
    the_rest = perf_table[context.stocks_to_hold:]

    # 为了前十个股票进行购买
    for stock, perf in buy_list.iteritems():
        stock_weight = 1 / context.stocks_to_hold

        # Place order
        if data.can_trade(stock):
            order_target_percent(stock, stock_weight)

    # 不在名单里股票
    for stock, perf in the_rest.iteritems():
        # Place order
        if data.can_trade(stock):
            order_target_percent(stock, 0.0)


def analyze(context, perf):
    # 进行分析
    returns, positions, transactions = pf.utils.extract_rets_pos_txn_from_zipline(perf)
    pf.create_returns_tear_sheet(returns, benchmark_rets=None)


# 设定时间
start = pd.to_datetime('1999-11-18', utc=True)
end = pd.to_datetime('2018-03-17', utc=True)


# 进行回测
result = run_algorithm(
    start=start,
    end=end,
    initialize=initialize,
    analyze=analyze,
    capital_base=10000,
    data_frequency='daily',
    bundle='quandl'
)


# 查看 输出里面的列
for column in result:
    print(column)


# Inspecting the first days' exposure
result.gross_leverage.head()


# 获取一个时间的输出
print(result.loc['2010-11-17'])


# Select day to view
day = '2009-03-17'

# Get portfolio value and positions for this day
port_value = result.loc[day, 'portfolio_value']
day_positions = result.loc[day, 'positions']

# 创建空的frame
df = pd.DataFrame(columns=['value', 'pnl'])

# Populate DataFrame with position info
for pos in day_positions:
    ticker = pos['sid'].symbol
    df.loc[ticker, 'value'] = pos['amount'] * pos['last_sale_price']
    df.loc[ticker, 'pnl'] = df.loc[ticker, 'value'] - (pos['amount'] * pos['cost_basis'])

# Add cash position
df.loc['cash', ['value', 'pnl']] = [(port_value - df['value'].sum()), 0]

# Make pie chart for allocations
fig, ax1 = plt.subplots(figsize=[12, 10])
ax1.pie(df['value'], labels=df.index, shadow=True, startangle=90)
ax1.axis('equal')
ax1.set_title('Allocation on {}'.format(day))
plt.show()

# Make bar chart for open PnL
fig, ax1 = plt.subplots(figsize=[12, 10])
pnl_df = df.drop('cash')
ax1.barh(pnl_df.index, pnl_df['pnl'], align='center', color='green', ecolor='black')
ax1.set_title('Open PnL on {}'.format(day))
plt.show()


df.loc[df['gross_leverage'] > 1.02, 'gross_leverage'] = 1.01


# Custom Time Series Analysis



# Format for book image
font = {'family': 'eurostile',
        'weight': 'normal',
        'size': 16}
rc('font', **font)

# Settings
calc_window = 126
year_length = 252

# Copy the columns we need
df = result.copy().filter(items=['portfolio_value', 'gross_leverage'])


# Function for annualized return
def ann_ret(ts):
    return np.power((ts[-1] / ts[0]), (year_length / len(ts))) - 1


# Function for drawdown
def dd(ts):
    return np.min(ts / np.maximum.accumulate(ts)) - 1


# Get a rolling window
rolling_window = result.portfolio_value.rolling(calc_window)

# Calculate rolling analytics
df['annualized'] = rolling_window.apply(ann_ret)
df['drawdown'] = rolling_window.apply(dd)

# Drop initial n/a values
df.dropna(inplace=True)

# Make a figure
fig = plt.figure(figsize=(12, 12))

# Make the base lower, just to make the graph easier to read
df['portfolio_value'] /= 100

# First chart
ax = fig.add_subplot(411)
ax.set_title('Strategy Results')
ax.plot(df['portfolio_value'],
        linestyle='-',
        color='black',
        label='Equity Curve', linewidth=3.0)

# Set log scale
ax.set_yscale('log')

# Make the axis look nicer
ax.yaxis.set_ticks(np.arange(df['portfolio_value'].min(), df['portfolio_value'].max(), 500))
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))

# Add legend and grid
ax.legend()
ax.grid(False)

# Second chart
ax = fig.add_subplot(412)
ax.plot(df['gross_leverage'],
        label='Strategy exposure'.format(calc_window),
        linestyle='-',
        color='black',
        linewidth=1.0)

# Make the axis look nicer
ax.yaxis.set_ticks(np.arange(df['gross_leverage'].min(), df['gross_leverage'].max(), 0.02))
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.2f'))

# Add legend and grid
ax.legend()
ax.grid(True)

# Third chart
ax = fig.add_subplot(413)
ax.plot(df['annualized'],
        label='{} days annualized return'.format(calc_window),
        linestyle='-',
        color='black',
        linewidth=1.0)

# Make the axis look nicer
ax.yaxis.set_ticks(np.arange(df['annualized'].min(), df['annualized'].max(), 0.5))
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))

# Add legend and grid
ax.legend()
ax.grid(True)

# Fourth chart
ax = fig.add_subplot(414)
ax.plot(df['drawdown'],
        label='{} days max drawdown'.format(calc_window),
        linestyle='-',
        color='black',
        linewidth=1.0)

# Make the axis look nicer
ax.yaxis.set_ticks(np.arange(df['drawdown'].min(), df['drawdown'].max(), 0.1))
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))

# Add legend and grid
ax.legend()
ax.grid(True)
