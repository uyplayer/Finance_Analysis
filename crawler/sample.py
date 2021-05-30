#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import requests
from bs4 import BeautifulSoup
import datetime
import dateparser
import time
import random
import pandas as pd

random.seed(444)

URL = "https://www.google.com/search?q=Goldman+Sachs&newwindow=1&safe=active&hl=en&tbs=cdr:1,cd_min:1/1/2011,cd_max:1/2/2021&source=lnms&tbm=nws&sa=X&ved=2ahUKEwiljv2XqajwAhXx-ioKHXGPAvoQ_AUoAXoECAEQAw&biw=1440&bih=821"

proxy_list= ['https://8.210.71.64:3128','https://8.210.71.64:3128']
# PROXY = random.choice(proxy_list)

PROXY = "127.0.0.1:8888"

proxies={
'http':PROXY,
'https':PROXY
}

headers_list =[{'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
               'Accept - Encoding':'gzip, deflate',
               'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
               'Connection':'Keep-Alive',
               'Host':'zhannei.baidu.com',
               'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'},{"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}]

headers = random.choice(headers_list)
print(headers)
page = 1

all = []
while URL:
    print("*" * 100)
    print("page : ", page)
    page = page + 1

    time.sleep(random.randint(1, 6))

    result = requests.get(URL, headers=headers, proxies=proxies)
    print("status code : ",result.status_code)
    content = result.content
    soup = BeautifulSoup(content, 'html.parser')
    link = soup.find_all('a', {'id': 'pnnext'})
    if link:
        URL = "https://www.google.com/"+link[0]['href']
    else:
        URL = link
    for item in soup.find_all("div", {"class": "dbsr"}):
        sub = []
        title = item.find('div', attrs={'class': 'JheGif'}).text
        title = title.replace('\n', '')
        date = item.find("span", attrs={'class': "WG9SHc"}).text
        date = dateparser.parse(date)
        date = date.strftime("%Y-%d-%m")
        print(title)
        print(date)
        sub.append(date)
        sub.append(title)
        all.append(sub)
    print("*" * 100)

print(all)

df = pd.DataFrame(all, columns=['Date', 'Title'])
print(df)

