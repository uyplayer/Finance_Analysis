#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   uyplayer
@License :   (C) Copyright 2013-2021, uyplayer.com
@Contact :   {uyplayer@qq.com}
@Software:   PyCharm
@File    :   main.py.py
@Time    :   2021/5/7 5:23 PM
@Desc    :
'''
import json

from flask import Flask
from flask_cors import CORS
import sys
import optparse
import time
from flask import request
import sys
from finbert import predict
from pytorch_pretrained_bert.modeling import BertForSequenceClassification
from transformers import AutoModelForSequenceClassification
import nltk

nltk.download('punkt')
app = Flask(__name__)
CORS(app)
start = int(round(time.time()))
model_path = "/Users/uyplayer/Projects/Finance_Analysis/sentiment_analysis/models"
model = AutoModelForSequenceClassification.from_pretrained(model_path, num_labels=3, cache_dir=None)

@app.route("/",methods=['POST','GET'])
def score():
    text=request.values.get("text")
    print(text)
    result = predict(text,model)
    print(type(result['prediction']))
    print(result['prediction'])
    return json.dump(result)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
