#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   uyplayer
@License :   (C) Copyright 2013-2021, uyplayer.com
@Contact :   {uyplayer@qq.com}
@Software:   PyCharm
@File    :   my_twin.py
@Time    :   2021/5/2 5:27 PM
@Desc    :
'''

import twint

c = twint.Config()

c.Search = "bitcoin"
c.Output = "../data/2013-01-07-2014-01-07-BTC_tweets.csv"
c.Store_csv = True
c.Lang = "en"
c.Since = "2013-01-07"
c.Until = "2014-01-07"
# c.Until = "2021-05-02"
c.Custom["tweet"] = ["date", "username","name","tweet","link"]

twint.run.Search(c)

