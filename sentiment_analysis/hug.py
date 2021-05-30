#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   uyplayer
@License :   (C) Copyright 2013-2021, uyplayer.com
@Contact :   {uyplayer@qq.com}
@Software:   PyCharm
@File    :   hug.py
@Time    :   2021/5/7 1:25 AM
@Desc    :
'''

from transformers import AutoModelForSequenceClassification
from finbert import predict
import argparse
import os

test = ["The investments and operational changes enable additional optimisation of the working hours and thereby further cost savings of some 7 % -9 %","Okmetic 's products are based on high-tech expertise that generates added value for customers , innovative product development and an extremely efficient production process .","Shareholder 's full name and ID code : - Petri Ailus , born 15.9.1966 For further information , please contact Isto Hantila , CEO , tel. +358 9 591 8342 .","9 September 2010 - Finnish stationery and gift retailer Tiimari HEL : TII1V said today its net sales rose by 2 % year-on-year to EUR5 .7 m in August 2010 , driven by growth in Finland , while demand in the Baltics remained weak .","By 14:29 CET on Monday , shares in Bavarian Nordic had climbed 1.21 % to DKK250 on the stock exchange in Copenhagen after having lost 7.41 % in the past month .","Mobile phone sales rose 25 % to 5.87 billion euros , while enterprise solution sales dropped 39 % to 186 million euros ."]

model_path = "/Users/uyplayer/Projects/Finance_Analysis/sentiment_analysis/models"
model = AutoModelForSequenceClassification.from_pretrained(model_path,num_labels=3,cache_dir=None)

result = predict("At this growth rate , paying off the national debt will be extremely painful .",model)
print(result['prediction'])