# -*- encoding: utf8-*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import random
import pymysql
# from sqlalchemy import create_engine


Stockiid = {'台泥': '1101'}
# 取得所有股票代碼
tmp_list = Stockiid.values()
stock_iids = []
for i in tmp_list:
    stock_iids.append(i)

headerlist = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991",
           "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 OPR/42.0.2393.94",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36 OPR/47.0.2631.39",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
           "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
           "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
           "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
           "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
           "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",
           "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"]

# 損益表
def get_html_one(id, time):
    id = int(id)
    user_agent = random.choice(headerlist)
    headers = {'User-Agent': user_agent}
    url = 'https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=IS_M_QUAR&LAST_RPT_CAT=IS_M_QUAR&STOCK_ID=%d&QRY_TIME=%d' % (
    id, time)
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    a = soup.select('div[id="divFinDetail"]')
    df_list = pd.read_html(str(a[0]))
    df = pd.DataFrame(df_list[0])
    df = df.drop(np.arange(2, df.shape[1], 2), axis=1)
    df = df.drop([1], axis=0).set_index(0)
    df_bb = df.loc[["營業毛利", "稅後淨利"]].T
    df_aa = df.loc["本業獲利"].str.replace('Q', '')
    df = pd.concat([df_aa, df_bb], axis=1, ignore_index=False, join="inner").T
    return df


# 資產負載表
def get_html_one2(id, time):
    id = int(id)
    user_agent = random.choice(headerlist)
    headers = {'User-Agent': user_agent}
    url = 'https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=BS_M_QUAR&STOCK_ID=%d&QRY_TIME=%d' % (id, time)
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    a = soup.select('div[id="divFinDetail"]')
    df_list = pd.read_html(str(a[0]))
    df = pd.DataFrame(df_list[0])
    df = df.drop(np.arange(2, df.shape[1], 2), axis=1)
    df = df.drop([1], axis=0).set_index(0)
    df = df.loc[['資產',  '資產總額', '流動資產合計', '流動負債合計', '負債總額', '股本合計']]
    return df

# roa roe
def get_html_one3(id, time):
    id = int(id)
    user_agent = random.choice(headerlist)
    headers = {'User-Agent': user_agent}
    url = 'https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=XX_M_QUAR&STOCK_ID=%d&QRY_TIME=%d' % (id, time)
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    a = soup.select('div[id="divFinDetail"]')
    df_list = pd.read_html(str(a[0]))
    df = pd.DataFrame(df_list[0])
    df = df.set_index(0)
    df = df.loc[["獲利能力","應收帳款週轉率 (次/年)", "資產報酬率 (當季)","股東權益報酬率 (當季)", "速動比","每股淨值 (元)"]]
    return df

# 資料表格合併
# 時間要改20194=>2019Q4
i = 1
l = len(stock_iids)
stop_list = []
for stock_iid in stock_iids:
    try:
        df1 = get_html_one(stock_iid, 20201)
        time.sleep(random.randint(5,10))
        try:
            df2 = get_html_one(stock_iid, 20182)
        except:
            df2 = pd.DataFrame()
        time.sleep(random.randint(5,10))
        try:
            df3 = get_html_one2(stock_iid, 20201)
        except:
            df3 = pd.DataFrame()
        time.sleep(random.randint(5,10))
        try:
            df4 = get_html_one2(stock_iid, 20182)
        except:
            df4 = pd.DataFrame()
        time.sleep(random.randint(5,10))
        try:
            df5 = get_html_one3(stock_iid, 20201)
        except:
            df5 = pd.DataFrame()
        time.sleep(random.randint(5,10))
        try:
            df6 = get_html_one3(stock_iid, 20173)
            df6 = df6.drop(np.arange(5, df6.shape[1] + 1), axis=1)
        except:
            df6 = pd.DataFrame()
        time.sleep(random.randint(5,10))
        df_cb_Income_statement = pd.concat([df1, df2], axis=1, ignore_index=True, join="outer")
        df_cb_Balance_sheet = pd.concat([df3, df4], axis=1, ignore_index=True, join="outer")
        df_roae = pd.concat([df5, df6], axis=1, ignore_index=True, join="outer")
        df_cb = pd.concat([df_cb_Income_statement,df_cb_Balance_sheet, df_roae], axis=0, ignore_index=False,
                          join="inner")
        df_cb.loc["股票代號"] = stock_iid
        df_total = df_cb.loc[["股票代號","本業獲利","稅後淨利","資產總額", "營業毛利", "應收帳款週轉率 (次/年)", "資產報酬率 (當季)", \
                           "股東權益報酬率 (當季)",'流動資產合計', '流動負債合計', "速動比", '負債總額',"每股淨值 (元)",'股本合計']]
        df_total = df_total.T
        df_total_final = df_total.set_axis(['stockiid','season','net_income','total_assets','operating_margin','account_receivable_rate','ROA',\
                                       'ROE','current_assets','current_liabilities','quick_ratio','total_debts','stock_price_per','share_capital'], axis=1, inplace=False)
        print(df_total_final)
        connection = pymysql.connect(host='127.0.0.1', user='root', password='0918554022', db='Project_test')
        cursor = connection.cursor()
        cols = "`,`".join([str(i) for i in df_total_final.columns.tolist()])
        for i, row in df_total_final.iterrows():
            sql = "INSERT INTO `basic_test` (`" + cols + "`) VALUES (" + "%s," * (len(row) - 1) + "%s)"
            cursor.execute(sql, tuple(row))
            connection.commit()
        connection.close()
        i = i + 1
        k = i / l
        print("股票代碼:%s，第%d支完成，完成比例:%f is ok" % (stock_iid, i - 1, k))
    except:
        stop_list = stop_list.append(stock_iid)
        print("股票代碼:%s，第%d支未完成，完成比例:%f is ok" % (stock_iid, i - 1, k))
print(stop_list)


# # 丟資料進資料庫
# # 方法一
# connection = pymysql.connect(host='127.0.0.1', user='root', password='0918554022', db='Project_test')
# cursor = connection.cursor()
# cols = "`,`".join([str(i) for i in df_total_final.columns.tolist()])
# for i, row in df_total_final.iterrows():
#     sql = "INSERT INTO `basic_test` (`" + cols + "`) VALUES (" + "%s," * (len(row) - 1) + "%s)"
#     cursor.execute(sql, tuple(row))
#     connection.commit()
# sql = "SELECT * FROM `basic_test`"
# cursor.execute(sql)
# result = cursor.fetchall()
# for i in result:
#     print(i)
# connection.close()


# # 方法二
# db_data = 'mysql+mysqlconnector://' + 'root' + ':' + '0000' + '@' + 'localhost' + ':3306/' + 'Project_test' + '?charset=utf8mb4'
# engine = create_engine(db_data)
# connection = pymysql.connect(host='localhost', user='root', password='0000', db='Project_test')
# cursor = connection.cursor()
# df_total_final.to_sql('basic_test', engine, if_exists='append', index=False)
# sql = "SELECT * FROM `basic_test`"
# cursor.execute(sql)
# result = cursor.fetchall()
# for i in result:
#     print(i)
# engine.dispose()
# connection.close()



