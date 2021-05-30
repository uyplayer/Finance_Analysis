#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   uyplayer
@License :   (C) Copyright 2013-2021, uyplayer.com
@Contact :   {uyplayer@qq.com}
@Software:   PyCharm
@File    :   lstm-seq2seq.py
@Time    :   2021/5/14 9:29 AM
@Desc    :
'''

import numpy as np
import pandas as pd
import time

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
"""
multi lstm layer in the models
Dropout
linear
"""
# Get model
class Model(Model):
  def __init__(self):
    super(Model, self).__init__()
    self.lstm = layers.LSTM(40)
    self.drop = layers.Dropout(0.2,input_shape=(40,))
    self.last = layers.Dense(1)

  def call(self, x):
    x = tf.reshape(x,[1,x.shape[0],-1])
    x = self.lstm(x)
    x = self.drop(x)
    x = self.last(x)
    return x

# Instantiate an optimizer to train the model.
model = Model()
optimizer = keras.optimizers.SGD(learning_rate=1e-3)
# Instantiate a loss function.
loss_fn = keras.losses.MeanAbsoluteError()

# Prepare the metrics.
train_acc_metric = keras.metrics.MeanAbsoluteError()
val_acc_metric = keras.metrics.MeanAbsoluteError()


epochs =100
timestamp = 5

for epoch in range(epochs):
    print("\nStart of epoch %d" % (epoch,))
    start_time = time.time()

    # Iterate over the batches of the dataset.
    for k in range(0, VAE_data.shape[0] - timestamp - 1):
        if timestamp + k <= VAE_data.shape[0]:
            x = VAE_data[k:timestamp + k, :]
            y = VAE_data[timestamp + k + 1, 3:4]
            x = tf.convert_to_tensor(x)
            x = tf.reshape(x, [1, x.shape[0], -1])
        with tf.GradientTape() as tape:
            logits = model(x, training=True)
            loss_value = loss_fn(y, logits)
        grads = tape.gradient(loss_value, model.trainable_weights)
        optimizer.apply_gradients(zip(grads, model.trainable_weights))

        # Update training metric.
        train_acc_metric.update_state(y, logits)

        # Log every 200 batches.
        if k % 200 == 0:
            print(
                "Training loss (for one batch) at step %d: %.4f"
                % (k, float(loss_value))
            )
            print("Seen so far: %d samples" % ((k + 1) * timestamp))

    # Display metrics at the end of each epoch.
    train_acc = train_acc_metric.result()
    print("Training acc over epoch: %.4f" % (float(train_acc),))

    # Reset training metrics at the end of each epoch
    train_acc_metric.reset_states()

    # Run a validation loop at the end of each epoch.
    # for x_batch_val, y_batch_val in val_dataset:
    #     val_logits = model(x_batch_val, training=False)
    #     # Update val metrics
    #     val_acc_metric.update_state(y_batch_val, val_logits)
    # val_acc = val_acc_metric.result()
    # val_acc_metric.reset_states()
    # print("Validation acc: %.4f" % (float(val_acc),))
    # print("Time taken: %.2fs" % (time.time() - start_time))