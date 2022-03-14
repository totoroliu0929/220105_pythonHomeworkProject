from spider import Spider,Data
import time

x = Spider("2330")
#x.getGrossMargin() #取得毛利率
#x.getEps() #取得eps
#x.getProfile() #取得基本資料
x.gerDividend() #取得股利資料
#x.getCompany() #取得上市公司名單
#x.getPrice() #取得收盤價

#Spider().getCompany()
Data().updateCompanyInfo() #抓取所有上市公司的資料，會執行很久


conn = Data().createConnection()
with conn:
    Data().getStockData(conn, '12330')
    Data().checkCount(conn, '12330')

print(time.gmtime())
print(int("{:0<4}{:0<2}{:0<2}".format(time.gmtime().tm_year,time.gmtime().tm_mon,time.gmtime().tm_mday)))