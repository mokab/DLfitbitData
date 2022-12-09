#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import requests
from datetime import datetime as dt
from datetime import timedelta
import time
import pickle
import glob
import yaml

with open('token.yml') as file:
    stng = yaml.safe_load(file)
token=stng['token']

headers = {'accept': 'application/json',
           'Authorization': 'Bearer %s'%token,
          }

# 日付条件の設定
strdt = dt.strptime("2021-09-11", '%Y-%m-%d')  # 開始日
#enddt = dt.strptime("2022-05-30", '%Y-%m-%d')  # 終了日
enddt = dt.today()
#days_num = (enddt - strdt).days + 1 
days_num = (enddt - strdt).days
datelist = [(strdt + timedelta(days=x)).strftime('%Y-%m-%d') for x in range(days_num)]

flist = glob.glob("./hrdata/*")
filehave = list(map(lambda x: x.split('/hd')[-1].split('.pkl')[0], flist))

datelist = list(set(datelist) - set(filehave))
datelist.sort()

for dd in datelist:
    requrl = 'https://api.fitbit.com/1/user/-/activities/heart/date/%s/1d/1sec.json' %dd
    bresponse = requests.get(requrl, headers=headers, verify=False)
    if bresponse.ok:
        with open('./hrdata/hd%s.pkl'%dd, 'wb') as f:
            pickle.dump(bresponse, f)
    else:
        time.sleep(3600)
    time.sleep(2)
    print(bresponse)
    print(dd)

