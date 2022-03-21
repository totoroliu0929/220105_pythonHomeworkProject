import time

from models import Spider,GetData
import tkinter as tk
from tkinter import ttk
from datetime import datetime

class Window(tk.Tk):
    def __init__(self):
        super().__init__()

        #上方的Frame=========start
        topFrame = tk.Frame(self,background='red')
        tk.Label(topFrame,text="存股輔助系統",font=("arial",20)).pack()
        topFrame.grid(column=0,row=0,columnspan=3,padx=20,pady=20)
        #上方的Frame=========end
        self.mainLabelFrame = MainLabelFrame(self,text="左邊的")
        self.mainLabelFrame.grid(column=0,row=1,padx=20,pady=20)
        self.updateStockData()

    def updateStockData(self):
        now = datetime.now()
        nowString = now.strftime("%Y-%m-%d %H:%M:%S")
        self.mainLabelFrame.updateStockScreen()
        self.mainLabelFrame.configure(text=nowString)
        self.after(60 * 1000, self.updateStockData)

class MainLabelFrame(tk.LabelFrame):
    def __init__(self, *args , **kwargs):
        super().__init__(*args, **kwargs)
        topFrame = tk.Frame(self,background='gray')
        tk.Label(topFrame, text="正常租借站點", font=("arial", 20),background='gray',fg="white").pack(padx=10,pady=10)
        #normal_count = dataSource.get_count_of_normal()
        tk.Label(topFrame, text=f"數量:",background='gray',fg='#ffffff', font=("arial",20)).pack(padx=10,pady=10)
        #topFrame.pack(pady=20)
        self.treeViewStock = ttk.Treeview(self,columns=('id','name','classification','d_yield','price','5y_EPS','5y_yield','5y_yield2','judge'),show="headings")
        self.treeViewDividend = ttk.Treeview(self,columns=('year','income','gross_profit','gross_margin','EPS','cash_dividends','stock_dividends'),show="headings")
        self.createTreeViewStock()

    def createTreeViewDividend(self,id):
        topFrame = tk.Frame(self)
        topFrame.pack()
        box = tk.Label(topFrame, text=f"現在股價：{Spider(id).getPriceNow()}")
        box.grid(column=0, row=0,padx=10, pady=10)
        tk.Label(topFrame, text=f"現在股價：{Spider(id).getPriceNow()}").grid(column=0, row=1,padx=10, pady=10)
        tk.Button(topFrame, text=f"現在股價：{Spider(id).getPriceNow()}").grid(column=1, row=0,padx=10, pady=10)
        #self.infoLabelFrame = InfoLabelFrame(topFrame, text="左邊的")
        #self.infoLabelFrame.pack(column=0, row=1, padx=20, pady=20)

        treeViewDividend = self.treeViewDividend
        treeViewDividend.heading('year',text='年')
        treeViewDividend.heading('income', text='收益')
        treeViewDividend.heading('gross_profit', text='毛利')
        treeViewDividend.heading('gross_margin', text='毛利率')
        treeViewDividend.heading('EPS', text='每股盈餘')
        treeViewDividend.heading('cash_dividends', text='現金股利')
        treeViewDividend.heading('stock_dividends', text='股票股利')

        treeViewDividend.column('year',width=100)
        treeViewDividend.column('income',width=100)
        treeViewDividend.column('gross_profit',width=100)
        treeViewDividend.column('gross_margin',width=100)
        treeViewDividend.column('EPS',width=100)
        treeViewDividend.column('cash_dividends',width=100)
        treeViewDividend.column('stock_dividends',width=100)
        treeViewDividend.pack()
        self.updateDividendScreen(id)

        def updatePriceNow():
            box.configure(text=f"現在股價：{Spider(id).getPriceNow()},{time.gmtime().tm_min}")
            # self.box.pack(padx=10, pady=10)
            self.after(60 * 1000, updatePriceNow)

        updatePriceNow()

    def updateDividendScreen(self,id):
        for i in self.treeViewDividend.get_children():
            self.treeViewDividend.delete(i)
        response = GetData().getListDividend(id)
        for item in response:
            item = list(item)
            grossMargin = '無資料' if item[1] == 0 else round(item[2] / item[1] * 100)/100
            item[1] = '無資料' if item[1] == 0 else '{:,}'.format(item[1])
            item[2] = '無資料' if item[2] == 0 else '{:,}'.format(item[2])
            item.insert(3, grossMargin)
            item[4] = '無資料' if item[4] == 0 else round(item[4]*100) / 100
            self.treeViewDividend.insert('', 'end', values=item)

    def createTreeViewStock(self):
        treeViewStock = self.treeViewStock
        treeViewStock.heading('id',text='股號')
        treeViewStock.heading('name', text='股名')
        treeViewStock.heading('d_yield', text='現金殖利率')
        treeViewStock.heading('price', text='最近收盤價')
        treeViewStock.heading('classification', text='產類別')
        treeViewStock.heading('5y_EPS', text='五年平均每股盈餘')
        treeViewStock.heading('5y_yield', text='五年平均現金殖利率')
        treeViewStock.heading('5y_yield2', text='五年平均股票股利')
        treeViewStock.heading('judge', text='價位')

        treeViewStock.column('id',width=100)
        treeViewStock.column('name',width=100)
        treeViewStock.column('d_yield',width=100)
        treeViewStock.column('price', width=100)
        treeViewStock.column('classification', width=100)
        treeViewStock.column('5y_EPS', width=100)
        treeViewStock.column('5y_yield', width=100)
        treeViewStock.column('5y_yield2', width=100)
        treeViewStock.column('judge', width=100)
        treeViewStock.pack()

    def checkStock(self,event):
        for item in self.treeViewStock.selection():
            item_text = self.treeViewStock.item(item, "values")
            print(item_text[0])
        self.treeViewStock.pack_forget()
        self.createTreeViewDividend(item_text[0])
        return

    def updateStockScreen(self):
        for i in self.treeViewStock.get_children():
            self.treeViewStock.delete(i)
        response = GetData().getListStock()
        for item in response:
            item = list(item)
            #print("yyyy",item[0])
            r = GetData().getSumInfo(item[0])
            x = [0,0,0]
            for i in r:
                #print(i)
                #print("VVVVV",x[0],x[1],x[2])
                x[0] += i[0]*100
                x[1] += i[1]*100
                x[2] += i[2]*100

            x[0] = x[0] / 1000
            x[1] = x[1] / 1000
            x[2] = x[2] / 1000
            item.append(x[0])
            item.append(round(x[1]*10000/item[4])/100)
            item.append(x[2])
            y = ""
            if item[3]>=10:
                y = "超低"
            elif item[3] >= 6.6:
                y = "便宜"
            elif item[3] >= 5:
                y = "合理"
            item.append(y)
            self.treeViewStock.insert('', 'end', values=item)
            self.treeViewStock.bind("<ButtonRelease-1>", self.checkStock)


if __name__=="__main__":
    window = Window()
    window.title("存股輔助系統")
    window.mainloop()