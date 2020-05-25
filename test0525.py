import requests,time, random, aaa, json
from bs4 import BeautifulSoup
from datetime import datetime
import pymysql
import Stockiid

#main 函數是抓上市公司的三大法人進出資料
def main():
#建立MySQL的連線
    db = pymysql.connect(host='localhost', user='dbuser', passwd='aabb1234', db='Project_test', port=3306, charset='utf8')
    cursor = db.cursor() #建立游標
    db.autocommit(True)

    tmp_list = Stockiid.Stockiid.values()
    stock_iids = []
    for i in tmp_list:
        i = i.replace(' ', '')
        stock_iids.append(i)

    T=(aaa.create_assist_date("20200518"))
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

#到公開資訊觀測站抓上市公司的三大法人進出資料
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
#確認股票都在股票清單stockiid裡面
            if len(stockiid) == 4:
                abc = [stockiid, ddd, foreign_investment, investment_bank, local_company]
                abc[2] = (abc[2].replace(',', ''))
                abc[3] = (abc[3].replace(',', ''))
                abc[4] = (abc[4].replace(',', ''))
                #print(abc)

#把資料塞進MySQL
                try:
                    if stockiid in stock_iids:
                        cursor.execute('INSERT INTO margin_trading_short_selling(stockiid, date, foreign_investment, investment_bank, local_company)' \
                                           '' 'VALUES(%s, %s, %s, %s, %s)', abc)

                except Exception as err:
                    print(err.args)

    db.commit()
    cursor.close()
    print('Done')

if __name__ == "__main__":
    main()

#main1 函數是抓上櫃公司的三大法人進出資料
def main1():
    # 取得所有股票代碼
    tmp_list = Stockiid.Stockiid.values()
    stock_iids = []
    for i in tmp_list:
        i = i.replace(' ', '')
        stock_iids.append(i)

    # 建立MySQL的連線
    db = pymysql.connect(host='localhost', user='dbuser', passwd='aabb1234', db='Project_test', port=3306,
                         charset='utf8')
    cursor = db.cursor()  # 建立游標
    db.autocommit(True)

    T = (aaa.create_assist_date())
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    
    #date是西元的時間，寫到T迴圈裡是把它改成民國的時間
    for t in T:
        date = datetime.strptime(str(t), '%Y%m%d').strftime('%Y-%m-%d')
        x = t[0:4] + '/' + t[4:6] + '/' + t[6:8]
        year = str(int(x[0:4]) - 1911)
        z = year + '/' + t[4:6] + '/' + t[6:8]
        url = "https://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_result.php?l=zh-tw&o=json&se=EW&t=D&d={}&s=0,asc".format(
            z)
        res = requests.get(url, headers=headers)
        # sleep_time = random.randint(2, 5)
        # time.sleep(sleep_time)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        soup_str = str(soup)
        jdata = json.loads(soup_str, encoding='big5')
        data = jdata["aaData"]

        for i in range(0, len(data)):
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
                        cursor.execute(
                            'INSERT INTO margin_trading_short_selling(stockiid, date, foreign_investment, investment_bank, local_company)' \
                            '' 'VALUES(%s, %s, %s, %s, %s)', abcd)

                except Exception as err:
                    print(err.args)

    db.commit()
    cursor.close()
    print('Done')

if __name__ == "__main__":
    main1()
