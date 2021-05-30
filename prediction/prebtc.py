#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   uyplayer
@License :   (C) Copyright 2013-2021, uyplayer.com
@Contact :   {uyplayer@qq.com}
@Software:   PyCharm
@File    :   prebtc.py
@Time    :   2021/5/10 7:27 PM
@Desc    :   prediction for btc
'''

'''
https://www.jeremyjordan.me/variational-autoencoders/
https://keras.io/examples/generative/vae/
'''

import time
import numpy as np
import pandas as pd
import os

# Pytorch
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.nn.functional as F
import torchvision
from torchsummary import summary
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
from torch.utils.data import TensorDataset, DataLoader
# warnings
import warnings
warnings.filterwarnings("ignore")


import warnings
warnings.filterwarnings("ignore")

from prediction.utils import parser,get_technical_indicators,btc_data
from prediction.Autoencoders import dataloaders,VAE
from prediction.paramters import args


os.environ['KMP_DUPLICATE_LIB_OK']='True'

# GPU or CPU
is_available = torch.cuda.is_available()
device = torch.device("cuda:0" if is_available else "cpu")
if is_available:
    print(" GPU is avaliable")
    num_gpu = torch.cuda.device_count()
    print(" number of GPU is : ",num_gpu)
    current_gpu = torch.cuda.current_device()
    print(" current_gpu is : ", current_gpu)
    print(" device is :",device)

else:
    print(" GPU is not avaliable ")
    print(" CPU is  avaliable ")
    print(" device is :",device)



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
# print(VAE_data[:2])

# data loader
train_iter, test_iter,load_all,n_batches = dataloaders(VAE_data)

dataiter = iter(train_iter)
sample_x, sample_y = dataiter.next()

# print('Sample input: \n', sample_x.size())
# print('Sample input: \n', sample_y.size())

# test model
n_hidden=args.n_hidden # neurons in each layer
n_latent=args.n_latent
n_layers=args.n_layers # num of dense layers in encoder and decoder respectively
n_output=VAE_data.shape[1]
batch_size=args.batch_size
n_dim = VAE_data.shape[1]

# model
net = VAE(n_dim=n_dim,n_hidden=n_hidden, n_latent=n_latent, n_layers=n_layers, n_output=n_output, batch_size=batch_size, act_type='relu',training=True)
sample_x = sample_x.to(torch.float32)
# print(sample_x.shape)  #[64, 16]
# output = net(sample_x)
# print(output)

# train
lr=1e-1
# criterion = nn.KLDivLoss(size_average=False)

# Custom loss functions
def my_loss(output, target):
    output = torch.sum(output, 1)
    target = torch.sum(target, 1)
    loss = F.kl_div(output, target)
    return loss

optimizer = optim.Adam(net.parameters(), lr=lr)

# train
def train():
    print_period = args.n_epoch // 10
    start = time.time()
    training_loss = []
    validation_loss = []
    # Epoch
    for epoch in range(args.n_epoch):
        epoch_loss = 0
        epoch_val_loss = 0

        n_batch_train = 0
        for i, data in enumerate(train_iter):
            # data
            sample_x, sample_y = data
            sample_x = sample_x.to(torch.float32)
            sample_y = sample_y.to(torch.float32)
            n_batch_train += 1
            # output of model
            output_net = net(sample_x)
            # loss
            loss = my_loss(output_net, sample_y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            print(loss.item())
            # epoch_loss += np.mean(loss)

    torch.save(net.state_dict(), "../models/VAE.pth")

# train()


activation = {}
def get_activation(name):
    def hook(model, input, output):
        activation[name] = output.detach()
    return hook


net = VAE(n_dim=n_dim,n_hidden=n_hidden, n_latent=n_latent, n_layers=n_layers, n_output=n_output, batch_size=batch_size, act_type='relu',training=False)
net.load_state_dict(torch.load("../models/VAE.pth"))
# print(net)
net.out.register_forward_hook(get_activation('out'))

more_feature = []
for i, data in enumerate(load_all):
    sample_x, _ = data
    sample_x = sample_x.to(torch.float32)
    output = net(sample_x)
    for i in activation['out'].tolist():
        more_feature.append(i)
more_feature= np.array(more_feature)
print(more_feature.shape) # (2360, 400)


# lstm
gan_num_features = more_feature.shape[1]
sequence_length = 17






