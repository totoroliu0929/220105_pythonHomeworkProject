import requests
from bs4 import BeautifulSoup

r = requests.get("https://tw.stock.yahoo.com/quote/2634.TW/dividend")
soup = BeautifulSoup(r.text,"html.parser")
u = soup.select("#main-2-QuoteDividend-Proxy .table-body-wrapper li div.Ta\(start\)")
print(u[0])
print(len(u))
u2 = soup.select("#main-2-QuoteDividend-Proxy .table-body-wrapper li.List\(n\) div:nth-of-type(2) span")
print(u2[0])
print(len(u2))

u3 = soup.select("#main-2-QuoteDividend-Proxy .table-body-wrapper li.List\(n\) div:nth-of-type(3) span")
print(u3[0])
print(len(u3))
for item in u2:
    print(item.text)

"""
r = requests.get("https://www.ptt.cc/bbs/joke/index.html")
soup = BeautifulSoup(r.text,"html.parser")
u = soup.select("div.btn-group.btn-group-paging a")#上一頁按鈕的a標籤
url = "https://www.ptt.cc"+ u[1]["href"]
"""