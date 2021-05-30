#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   uyplayer
@License :   (C) Copyright 2013-2021, uyplayer.com
@Contact :   {uyplayer@qq.com}
@Software:   PyCharm
@File    :   Autoencoders.py
@Time    :   2021/5/10 8:23 PM
@Desc    :   Autoencoders for extract high level features
'''

# dependency library
from __future__ import print_function
# Pytorch
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
from torchsummary import summary
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader
from torch.distributions import Normal
from torch.utils.data import TensorDataset, DataLoader
# project lib
from prediction.paramters import args
# warnings
import warnings
warnings.filterwarnings("ignore")



def dataloaders(VAE_data):

    batch_size = args.batch_size
    num_training_days = args.num_training_days
    n_batches = VAE_data.shape[0] / batch_size
    # create Tensor datasets
    train_data = TensorDataset(torch.from_numpy(VAE_data[:num_training_days,:]), torch.from_numpy(VAE_data[:num_training_days,:]))
    valid_data = TensorDataset(torch.from_numpy(VAE_data[num_training_days:,:]), torch.from_numpy(VAE_data[num_training_days:,:]))

    load_all = TensorDataset(torch.from_numpy(VAE_data), torch.from_numpy(VAE_data))
    # make sure to SHUFFLE your data
    train_loader = DataLoader(train_data, shuffle=True, batch_size=batch_size)
    valid_loader = DataLoader(valid_data, shuffle=True, batch_size=batch_size)
    load_all = DataLoader(load_all, shuffle=True, batch_size=batch_size)

    return train_loader,valid_loader,load_all,n_batches


class VAE(nn.Module):
    def __init__(self,n_dim,n_hidden=400, n_latent=2, n_layers=1, n_output=784,batch_size=100, act_type='relu',training=False,):
        super(VAE, self).__init__()

        self.training=training
        if act_type != "relu":
            raise Exception("you must use rele as activation function")
        self.Encoder = nn.Sequential(nn.Linear(n_dim, n_hidden,
                                     nn.ReLU()),
                                     nn.Linear(n_hidden, n_hidden),
                                     nn.Linear(n_hidden, n_hidden),
                                     nn.Linear(n_hidden, n_latent * 2))


        self.Decoder = nn.Sequential(nn.Linear(n_latent, n_hidden,
                                               nn.ReLU()),
                                     nn.Linear(n_hidden, n_hidden),
                                     nn.ReLU()
                                     )

        self.out = nn.Linear(n_hidden, n_hidden)
        self.relu = nn.ReLU()
        self.last = nn.Linear(n_hidden, n_output)
        self.sig = nn.Sigmoid()


        self.z_mean = nn.Linear(n_latent * 2, n_latent)
        self.z_log_var = nn.Linear(n_latent * 2, n_latent)



    def reparameterize(self, mu, logvar):
        if self.training:

            v = torch.randn_like(0.5 * logvar)
            std = torch.exp(0.5 *v)
            eps = torch.randn_like(std)
            return eps.mul(std).add_(mu)
        else:
            return mu
    def forward(self, x):
        # encoder
        encoder_output = self.Encoder(x) #torch.Size([64, 4])

        # mean and war
        mean = self.z_mean(encoder_output)
        log_var = self.z_log_var(encoder_output)

        z = self.reparameterize(mean, log_var)
        z = self.Decoder(z)
        z = self.out(z)
        z = self.relu(z)
        z = self.last(z)
        z = self.sig(z)

        return z







