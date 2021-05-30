#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   uyplayer
@License :   (C) Copyright 2013-2021, uyplayer.com
@Contact :   {uyplayer@qq.com}
@Software:   PyCharm
@File    :   BBANDS.py
@Time    :   2021/4/21 9:18 PM
@Desc    : Bollinger Bands
'''

import talib
from talib import BBANDS
import numpy as np

close = np.random.random(100)
print(close)

upperband, middleband, lowerband = BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)

print(upperband)
print(middleband)
print(lowerband)