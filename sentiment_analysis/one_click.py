
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   uyplayer
@License :   (C) Copyright 2013-2021, uyplayer.com
@Contact :   {uyplayer@qq.com}
@Software:   PyCharm
@File    :   one_click.py
@Time    :   2021/5/7 5:53 PM
@Desc    :
'''

import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification

os.environ['KMP_DUPLICATE_LIB_OK']='True'

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")

model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

inputs = tokenizer("i do not like you", return_tensors="pt")
outputs = model(**inputs)

print(outputs)
