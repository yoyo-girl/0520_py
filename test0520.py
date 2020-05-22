import requests,time, aaa, json
from bs4 import BeautifulSoup
from datetime import datetime
import pymysql
import stockiid

#去抓stockid的所有台股目前股票代碼(20200521)

# 取得所有股票代碼
tmp_list = stockiid.Stockiid.values()
stock_iids = []
for i in tmp_list:
    i = i.replace(' ', '')
    stock_iids.append(i)

#建立MySQL的連線
db = pymysql.connect(host='localhost', user='dbuser', passwd='aabb1234', db='Project_test', port=3306, charset='utf8')
cursor = db.cursor() #建立游標
db.autocommit(True)

T=(aaa.create_assist_date())
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

for t in T:
    date = datetime.strptime(str(t), '%Y%m%d').strftime('%Y-%m-%d')
    x = t[0:4] +'/'+ t[4:6] +'/'+ t [6:8]
    year = str(int(x[0:4])-1911)
    z = year +'/'+ t[4:6] +'/'+ t [6:8]
    url = "https://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_result.php?l=zh-tw&o=json&se=EW&t=D&d={}&s=0,asc".format(z)
    # print(url)
    res = requests.get(url, headers=headers)
    # sleep_time = random.randint(2, 5)
    # time.sleep(sleep_time)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    soup_str = str(soup)
    jdata = json.loads(soup_str, encoding='big5')
    data = jdata["aaData"]

    for i in range(0,len(data)):
        a = data[i][0]
        if len(a) == 4:
            b = data[i][4]
            c = data[i][13]
            d = data[i][22]
            abcd = [a, date, b, c, d]
            abcd[2] = (abcd[2].replace(',', ''))
            abcd[3] = (abcd[3].replace(',', ''))
            abcd[4] = (abcd[4].replace(',', ''))
            # print(abcd)

            try:

                if a in stock_iids:
                    cursor.execute('INSERT INTO margin_trading_short_selling(stockiid, date, foreign_investment, investment_bank, local_company)' \
                                       '' 'VALUES(%s, %s, %s, %s, %s)', abcd)

            except Exception as err:
                print(err.args)


# db.commit()
# cursor.close()
# print('Done')