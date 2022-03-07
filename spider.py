import requests
from bs4 import BeautifulSoup

r = requests.get("https://tw.stock.yahoo.com/quote/2634.TW/dividend")
soup = BeautifulSoup(r.text,"html.parser")
u = soup.select("#main-2-QuoteDividend-Proxy .table-body-wrapper li div:nth-of-type(1)")
print(u[0])
print(len(u))

"""
r = requests.get("https://www.ptt.cc/bbs/joke/index.html")
soup = BeautifulSoup(r.text,"html.parser")
u = soup.select("div.btn-group.btn-group-paging a")#上一頁按鈕的a標籤
url = "https://www.ptt.cc"+ u[1]["href"]
"""