import requests,time, random, aaa, json
#import stockid
from bs4 import BeautifulSoup
from datetime import datetime
import pymysql
import stockiid

#建立MySQL的連線
db = pymysql.connect(host='localhost', user='dbuser', passwd='aabb1234', db='Project_test', port=3306, charset='utf8')
cursor = db.cursor() #建立游標
db.autocommit(True)

#確認抓下來的股票都有在股票清單裡嗎？
tmp_list = stockiid.Stockiid.values()
stock_iids = []
for i in tmp_list:
    i = i.replace(' ', '')
    stock_iids.append(i)

T=(aaa.create_assist_date())
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

for t in T:
    url = "https://www.twse.com.tw/fund/T86?response=json&date={}&selectType=ALLBUT0999".format(t)
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    soup_str = str(soup)
    jdata = json.loads(soup_str, encoding='big5')
    date = jdata['date']

    for j in range(0,len(jdata['data'])):
        stockiid = jdata['data'][j][0]
        foreign_investment = jdata['data'][j][4]
        investment_bank = jdata['data'][j][10]
        local_company = jdata['data'][j][11]
        ddd = datetime.strptime(str(date), '%Y%m%d').strftime('%Y-%m-%d')

        if len(stockiid) == 4:
            abc = [stockiid, ddd, foreign_investment, investment_bank, local_company]
            abc[2] = (abc[2].replace(',', ''))
            abc[3] = (abc[3].replace(',', ''))
            abc[4] = (abc[4].replace(',', ''))
            #print(abc)

            try:
                if stockiid in stock_iids:
                    cursor.execute('INSERT INTO margin_trading_short_selling(stockiid, date, foreign_investment, investment_bank, local_company)' \
                                       '' 'VALUES(%s, %s, %s, %s, %s)', abc)

            except Exception as err:
                print(err.args)


db.commit()
# cursor.close()
print('Done')
