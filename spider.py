import requests
from bs4 import BeautifulSoup
import urllib.request, csv, sqlite3, time
from sqlite3 import Error as sqlite3Error

class Spider:
    def __init__(self,id:str=None):
        self.id = id
        self.listProfile = dict()
        self.listDividend = dict()
        self.listEps = dict()
        self.listCompany = dict()

    def getProfile(self):
        r = requests.get("https://tw.stock.yahoo.com/quote/{}.TW/profile".format(self.id))
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            u1 = soup.select("#main-2-QuoteProfile-Proxy section:nth-of-type(1) span>span")
            u2 = soup.select("#main-2-QuoteProfile-Proxy section:nth-of-type(1) span+div")
            for i in range(len(u1)):
                #print(u1[i].text,u2[i].text)
                self.listProfile[u1[i].text] = u2[i].text
            return self.listProfile
        else:
            return None

    def getGrossMargin(self):
        r = requests.get("https://tw.stock.yahoo.com/quote/{}.TW/income-statement".format(self.id))
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            u1 = soup.select("#qsp-income-statement-table .table-header-wrapper > div")
            u2 = soup.select("#qsp-income-statement-table li:nth-of-type(1) span")
            u3 = soup.select("#qsp-income-statement-table li:nth-of-type(2) span")
            for i in range(1,len(u1)):
                x = float(u2[i].text.replace(",", ""))
                y = float(u3[i].text.replace(",", ""))
                print(u1[i].text,x,y,y/x)
        else:
            return None


    def gerDividend(self):
        r = requests.get("https://tw.stock.yahoo.com/quote/{}.TW/dividend".format(self.id))
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            u1 = soup.select("#main-2-QuoteDividend-Proxy .table-body-wrapper li div.Ta\(start\)")
            u2 = soup.select("#main-2-QuoteDividend-Proxy .table-body-wrapper li.List\(n\) div:nth-of-type(2) span")
            u3 = soup.select("#main-2-QuoteDividend-Proxy .table-body-wrapper li.List\(n\) div:nth-of-type(3) span")
            for i in range(len(u1)):
                #item = [u1[i].text,u2[i].text,u3[i].text]
                #self.listDividend.append(item)
                if u1[i].text[0:4:1] in self.listDividend:
                    self.listDividend[u1[i].text[0:4:1]]["次數"] += 1
                    self.listDividend[u1[i].text[0:4:1]]["現金股利"] += float(u2[i].text)
                    self.listDividend[u1[i].text[0:4:1]]["股票股利"] += float(u3[i].text)
                    print(u1[i].text,float(u2[i].text),float(u3[i].text))
                else:
                    self.listDividend[u1[i].text[0:4:1]] = {"年度":u1[i].text[0:4:1],"次數":1,"現金股利":float(u2[i].text),"股票股利":float(u3[i].text)}
                    print(u1[i].text, float(u2[i].text), float(u3[i].text))
            print(self.listDividend)
        else:
            return None

    def getEps(self):
        r = requests.get("https://tw.stock.yahoo.com/quote/{}.TW/eps".format(self.id))
        soup = BeautifulSoup(r.text, "html.parser")
        u1 = soup.select("#qsp-eps-table li.List\(n\)>div>div:nth-of-type(1)")
        u2 = soup.select("#qsp-eps-table li.List\(n\)>div>div:nth-of-type(2)")
        for i in range(len(u1)):
            if u1[i].text[0:4:1] in self.listEps:
                self.listEps[u1[i].text[0:4:1]]["次數"] += 1
                self.listEps[u1[i].text[0:4:1]]["每股盈餘"] += float(u2[i].text)
                print(u1[i].text,float(u2[i].text))
            else:
                self.listEps[u1[i].text[0:4:1]] = {"年度":u1[i].text[0:4:1], "次數":1, "每股盈餘":float(u2[i].text)}
                print(u1[i].text, float(u2[i].text))
        print(self.listEps)

    def getCompany(self):
        url = 'https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=open_data'
        webpage = urllib.request.urlopen(url)
        data = csv.reader(webpage.read().decode('utf-8').splitlines())
        for i in data:
            #print('證券代號->',i[0],'證券名稱=',i[1], '殖利率(%)=',i[2],'股利年度=',i[3], '本益比=',i[4],'股價淨值比=',i[5], '財報年/季=',i[6])
            self.listCompany[i[0]] = {'id':i[0],'name':i[1]}
        self.listCompany.pop('證券代號',0)


    def getPrice(self):
        url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=open_data'
        webpage = urllib.request.urlopen(url)
        data = csv.reader(webpage.read().decode('utf-8').splitlines())
        self.getCompany()
        for i in data:
            #print('證券代號->',i[0],'證券名稱=',i[1], '成交股數=',i[2], '成交金額=',i[3],'開盤價=',i[4], '最高價=',i[5],'最低價=',i[6], '收盤價=',i[7], '漲跌價差=',i[8], '成交筆數=',i[9])
            if i[0] in self.listCompany:
                self.listCompany[i[0]]['price']=i[7]
        #print(self.listCompany)
        return self.listCompany

class Data:
    def __init__(self):
        self.listInfo = Spider().getPrice()
        self.dbFile = 'yield.db'
        #print(self.listInfo)

    def createConnection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.dbFile)
        except sqlite3Error as e:
            print("sqlite連線錯誤")
            print(e)
            return
        return conn

    def createStockTable(self, conn):
        sql = '''
            CREATE TABLE IF NOT EXISTS stock(
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            price TEXT,
            time_to_market TEXT,
            classification TEXT,
            share_capital TEXT,
            IHOLD TEXT,
            update_time INTEGER,
            UNIQUE (name)
        );
            '''
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
        except sqlite3Error as e:
            print(e)

    def replaceStockData(self,conn, item):
        sql = '''
        INSERT or replace INTO 
        stock(id,name,price,time_to_market,classification,share_capital,IHOLD,update_time)
        VALUES( ?,?,?,?,?,?,?,?)
        '''

        try:
            curser = conn.cursor()
            id = item['id']
            name = item['name']
            price = item['price']
            time_to_market = item['time_to_market']
            classification = item['classification']
            share_capital = item['share_capital']
            IHOLD = item['IHOLD']
            update_time = item['update_time']
            curser.execute(sql, (id, name, price, time_to_market, classification, share_capital, IHOLD, update_time))
        except  sqlite3Error as e:
            print(e)
        conn.commit()

    def checkCount(self, conn, id):
        sql = '''
        SELECT count(*)
        FROM stock
        WHERE id = '{}'
        '''.format(id)
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            row = cursor.fetchone()
            #print(row[0])
        except sqlite3Error as e:
            print(e)
        return row[0]

    def getStockData(self, conn, id):
        sql = '''
                SELECT *
                FROM stock
                WHERE id = '{}'
                '''.format(id)
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            row = cursor.fetchone()
            print(row)
        except sqlite3Error as e:
            print(e)
        return row

    def updateCompanyInfo(self):
        import time
        for item in list(self.listInfo.values()):
            #print(item)
            conn = self.createConnection()
            update_time = int("{:0<4}{:0<2}{:0<2}".format(time.gmtime().tm_year,time.gmtime().tm_mon,time.gmtime().tm_mday))
            with conn:
                self.createStockTable(conn)
                ctype = 99
                stock = self.getStockData(conn, item['id'])
                if self.checkCount(conn, item['id']) == 0:
                    ctype = 0
                elif update_time - 7 > stock[7] or (time.gmtime().tm_mday % 5 == 0 and update_time != stock[7]):
                    ctype = 0
                elif update_time != stock[7]:
                    ctype = 1
                if ctype == 99:
                    return
                elif ctype == 0:
                    newInfo = Spider(item['id']).getProfile()
                    item['time_to_market'] = newInfo['上市時間'] or ""
                    item['classification'] = newInfo['產業類別'] or ""
                    item['share_capital'] = newInfo['股本'] or ""
                    item['IHOLD'] = newInfo['董監持股比例(%)'] or ""
                    time.sleep(1)
                else:
                    item['time_to_market'] = stock[3]
                    item['classification'] = stock[4]
                    item['share_capital'] = stock[5]
                    item['IHOLD'] = stock[6]
                item['update_time'] = update_time
                self.replaceStockData(conn, item)

"""
條件1：股本 > 50 億元以上

條件2：近 10 年平均現金股利發放率 > 50%

條件3：近 10 年平均現金股利殖利率 > 6%

條件4：近 10 年每年 EPS > 1 元以上

本益比= 股價/每股盈餘
"""