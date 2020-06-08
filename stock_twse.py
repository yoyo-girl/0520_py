
# coding: utf-8

# In[1]:


import requests, json, time, random, os
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


# In[2]:


date1 = ['20160101','20160202','20160301']


# In[3]:


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
url_List = []
for tt in date1:
    url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=%s&stockNo=2330" %tt
#     time.sleep(random.randint(0, 5))
    url_List.append(url)


# In[4]:


url_List


# In[20]:


jdata_List = []
for i in url_List:
    res = requests.get(i, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    jdata = json.loads(res.text, encoding='utf-8')
    jdata_List.append(jdata)


# In[21]:


jdata_List[0]


# In[22]:


for x in range(0,1):
    jdata_List[x]
    trade = {}
    for i in range(0, len(jdata['data'])):
        Date = jdata['data'][i][0]
        Vol = jdata['data'][i][1]
        Open = jdata['data'][i][3]
        High = jdata['data'][i][4]
        Low = jdata['data'][i][5]
        Close = jdata['data'][i][6]
        trade[Date]=[Open,High,Low,Close,Vol]
    print(trade)


# In[23]:


trade


# In[26]:


L = [l for l in Dic_Close.values()]


# In[27]:


def Moving_Average(interval = 5):
    Dic_MA = {}
    interval  =int(interval)
    for i in range(len(L)):
        if i-interval <0:
            pass
        else:
            Dic_MA[D[i]]="{:}".format(sum(L[i-interval:i])/interval)
    return Dic_MA


# In[25]:


def moving_average(a, n=5) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

for i in range(len(L)):
    M5 = moving_average(L[i])


# In[ ]:


M5 = Moving_Average (interval = 5)
M10 = Moving_Average (interval = 10)


# In[ ]:


# 把日期(key)取出來
m0 = [l for l in M5.keys()]
m5 = [l for l in M5.values()]
m10 = [l for l in M10.values()]

#Result_List1是多頭(MA5>MA10)
Result_List1= []

#Result_List3是空頭(MA5<MA10)
Result_List3= []


for i in range(10,len(m0)):
    difference = float(0.1)
    try:
        if float(m5[i]) - float(m10[i]) > difference:
            Result_List1.append(m0[i])
        if float(m5[i]) - float(m10[i]) < difference:
            Result_List3.append(m0[i])
    except IndexError as p:
        pass


# In[168]:


Result_Buy = set(Result_List0).intersection(set(Result_List1))


# In[169]:


Result_Sell = set(Result_List2).intersection(set(Result_List3))


# In[ ]:


D={}
for i in Result_Buy:
    D[i]=Dic_Close[i]

