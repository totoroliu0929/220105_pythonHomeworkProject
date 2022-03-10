import requests
from bs4 import BeautifulSoup
import urllib.request, csv

class spider:
    def __init__(self,id):
        self.id = id
        self.listDividend = dict()
        self.listEps = dict()

    def dividend(self):
        r = requests.get("https://tw.stock.yahoo.com/quote/{}.TW/dividend".format(self.id))
        soup = BeautifulSoup(r.text, "html.parser")
        u1 = soup.select("#main-2-QuoteDividend-Proxy .table-body-wrapper li div.Ta\(start\)")
        u2 = soup.select("#main-2-QuoteDividend-Proxy .table-body-wrapper li.List\(n\) div:nth-of-type(2) span")
        u3 = soup.select("#main-2-QuoteDividend-Proxy .table-body-wrapper li.List\(n\) div:nth-of-type(3) span")
        for i in range(len(u1)):
            #item = [u1[i].text,u2[i].text,u3[i].text]
            #self.listDividend.append(item)
            if u1[i].text[0:4:1] in self.listDividend:
                self.listDividend[u1[i].text[0:4:1]][1] += 1
                self.listDividend[u1[i].text[0:4:1]][2] += float(u2[i].text)
                self.listDividend[u1[i].text[0:4:1]][3] += float(u3[i].text)
                print(u1[i].text,float(u2[i].text),float(u3[i].text))
            else:
                self.listDividend[u1[i].text[0:4:1]] = [u1[i].text[0:4:1],1,float(u2[i].text),float(u3[i].text)]
                print(u1[i].text, float(u2[i].text), float(u3[i].text))
        print(self.listDividend)

    def eps(self):
        r = requests.get("https://tw.stock.yahoo.com/quote/{}.TW/eps".format(self.id))
        soup = BeautifulSoup(r.text, "html.parser")
        u1 = soup.select("#qsp-eps-table li.List\(n\)>div>div:nth-of-type(1)")
        u2 = soup.select("#qsp-eps-table li.List\(n\)>div>div:nth-of-type(2)")
        for i in range(len(u1)):
            if u1[i].text[0:4:1] in self.listEps:
                self.listEps[u1[i].text[0:4:1]][1] += 1
                self.listEps[u1[i].text[0:4:1]][2] += float(u2[i].text)
                print(u1[i].text,float(u2[i].text))
            else:
                self.listEps[u1[i].text[0:4:1]] = [u1[i].text[0:4:1],1,float(u2[i].text)]
                print(u1[i].text, float(u2[i].text))
        print(self.listEps)

    def company(self):
        url = 'https://www.twse.com.tw/exchangeReport/BWIBBU_d?response=open_data'
        webpage = urllib.request.urlopen(url)
        data = csv.reader(webpage.read().decode('utf-8').splitlines())
        for i in data:
            print('證券代號->',i[0],'證券名稱=',i[1], '殖利率(%)=',i[2],'股利年度=',i[3], '本益比=',i[4],'股價淨值比=',i[5], '財報年/季=',i[6])

    def price(self):
        url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=open_data'
        webpage = urllib.request.urlopen(url)
        data = csv.reader(webpage.read().decode('utf-8').splitlines())
        for i in data:
            print('證券代號->',i[0],'證券名稱=',i[1], '成交股數=',i[2], '成交金額=',i[3],'開盤價=',i[4], '最高價=',i[5],'最低價=',i[6], '收盤價=',i[7], '漲跌價差=',i[8], '成交筆數=',i[9])

spider("2330").dividend()
"""
r = requests.get("https://www.ptt.cc/bbs/joke/index.html")
soup = BeautifulSoup(r.text,"html.parser")
u = soup.select("div.btn-group.btn-group-paging a")#上一頁按鈕的a標籤
url = "https://www.ptt.cc"+ u[1]["href"]
"""


"""
條件1：股本 > 50 億元以上

條件2：近 10 年平均現金股利發放率 > 50%

條件3：近 10 年平均現金股利殖利率 > 6%

條件4：近 10 年每年 EPS > 1 元以上
"""