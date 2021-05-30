#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   uyplayer
@License :   (C) Copyright 2013-2021, uyplayer.com
@Contact :   {uyplayer@qq.com}
@Software:   PyCharm
@File    :   begain.py
@Time    :   2021/4/21 8:21 PM
@Desc    :
'''

import numpy as np
import talib
from talib import MA_Type,abstract
#
# close = np.random.random(100)
#
# print(close)
#
# output = talib.SMA(close)
# print(output)
#
# upper, middle, lower = talib.BBANDS(close, matype=MA_Type.T3)
# print(upper)
# print(middle)
# print(lower)
#
# output = talib.MOM(close, timeperiod=5)
# print(output)
#
# inputs = {
#     'open': np.random.random(100),
#     'high': np.random.random(100),
#     'low': np.random.random(100),
#     'close': np.random.random(100),
#     'volume': np.random.random(100)
# }

import talib

print(talib.get_functions())
print(talib.get_function_groups())