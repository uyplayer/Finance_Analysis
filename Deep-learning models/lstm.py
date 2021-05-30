#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   uyplayer
@License :   (C) Copyright 2013-2021, uyplayer.com
@Contact :   {uyplayer@qq.com}
@Software:   PyCharm
@File    :   lstm.py
@Time    :   2021/5/13 9:51 AM
@Desc    :
'''

import numpy as np
import pandas as pd


import tensorflow as tf
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras import Model


import warnings
warnings.filterwarnings("ignore")

from prediction.utils import parser,get_technical_indicators,btc_data
from prediction.Autoencoders import dataloaders,VAE
from prediction.paramters import args

# data
data_btc = btc_data()
indicators = get_technical_indicators(data_btc)
indicators = indicators.dropna()
indicators = indicators.reset_index(drop=True)
# 2014-10-07-2021-05-08
# print(indicators.columns.values.tolist())
# print(len(indicators.columns.values.tolist()))


VAE_data = indicators.drop("Date",  axis=1)
VAE_data = VAE_data.values
# print(VAE_data.shape) # (2360, 17)

feature_len = VAE_data.shape[1]
# train learnign rate
learning_rate = 1e-1

class Model(Model):
  def __init__(self):
    super(Model, self).__init__()
    self.lstm = layers.LSTM(10)
    self.last = layers.Dense(1)

  def call(self, x):
    x = tf.reshape(x,[1,x.shape[0],-1])
    x = self.lstm(x)
    x = self.last(x)
    return x


model = Model()
loss_object = tf.keras.losses.MeanAbsoluteError()
optimizer = tf.keras.optimizers.Adam()
timestamp = 5
epoch_time = 100
def train():
  for epoch in range(epoch_time):
    for k in range(0, VAE_data.shape[0] - timestamp - 1):
      if timestamp + k <= VAE_data.shape[0]:
        x = VAE_data[k:timestamp + k, :]
        y = VAE_data[timestamp + k + 1,3:4]
        x = tf.convert_to_tensor(x)
        print(x.shape)
        with tf.GradientTape() as tape:
          out = model(x)[0]
          loss = loss_object(out,y)
          print(loss.numpy(),out.numpy(),y)
        grads = tape.gradient(loss, model.trainable_weights)

        optimizer.apply_gradients(zip(grads, model.trainable_weights))

train()






















