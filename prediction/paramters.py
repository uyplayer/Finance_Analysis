#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   uyplayer
@License :   (C) Copyright 2013-2021, uyplayer.com
@Contact :   {uyplayer@qq.com}
@Software:   PyCharm
@File    :   paramters.py
@Time    :   2021/5/10 8:20 PM
@Desc    :   paramters
'''

# dependency library
from __future__ import print_function
# system
import argparse

parser = argparse.ArgumentParser()

# Autoencoders
parser.add_argument('-b_s',"--batch_size", type=int, default=64, help="batch_size")
parser.add_argument('-b_t_d',"--num_training_days", type=int, default=1900, help="num_training_days")
parser.add_argument('-n_h',"--n_hidden", type=int, default=400, help="n_hidden for autoencoder")
parser.add_argument('-n_l',"--n_latent", type=int, default=2, help="n_latent for autoencoder")
parser.add_argument('-n_la',"--n_layers", type=int, default=3, help="n_layers for autoencoder")
parser.add_argument('-n_e',"--n_epoch", type=int, default=1000, help="n_epoch for train")
args = parser.parse_args()