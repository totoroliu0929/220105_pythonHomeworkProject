import time
import tkinter

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
        #self.after(60 * 1000, self.updateStockData)

class MainLabelFrame(tk.LabelFrame):
    def __init__(self, *args , **kwargs):
        super().__init__(*args, **kwargs)
        topFrame = tk.Frame(self)
        topFrame.pack(pady=20)
        self.topFrame = topFrame

        self.treeViewStock = ttk.Treeview(self,columns=('id','name','classification','d_yield','price','5y_EPS','5y_yield','5y_yield2','judge'),show="headings")
        self.treeViewDividend = ttk.Treeview(self,columns=('year','income','gross_profit','gross_margin','EPS','cash_dividends','stock_dividends'),show="headings")
        self.treeViewProfit = ttk.Treeview(self, columns=('quarter', 'income', 'gross_profit', 'gross_margin', 'EPS'), show="headings")
        self.createTreeViewStock()
        self.createTopFrameObjects()

    def createTopFrameObjects(self):
        def checkSearch():
            if value.get() is False:
                message.configure(text="請填入有效的內容進行搜尋")
                return False
            return True
        def updateStockScreen_50():
            self.updateStockScreen(value=5)
        def updateStockScreen_66():
            self.updateStockScreen(value=6.6)
        def updateStockScreen_99():
            self.updateStockScreen(value=10)
        def searchId():
            if checkSearch() != False:
                self.updateStockScreen("id","=",f"{value.get()}")
        def searchName():
            if checkSearch() != False:
                self.updateStockScreen("name","like",f"'%{value.get()}%'")
        def searchPrice():
            if checkSearch() != False:
                self.updateStockScreen("price","<=",f"{value.get()}")
        topFrame = self.topFrame
        value = tk.StringVar()
        value.set("")
        message = tk.Label(topFrame, text="可利用以下欄位進行搜尋", anchor="center",width=36).grid(column=2, row=0, columnspan=2, pady=5)
        input = tk.Entry(topFrame, width=36, textvariable=value)
        input.grid(column=2, row=1, columnspan=2, pady=5)
        tk.Button(topFrame, text=f"搜尋股號", command=searchId, width=36, bd=0, fg="white", bg="black",height=2).grid(column=0, row=2, columnspan=2, pady=5)
        tk.Button(topFrame, text=f"搜尋股名", command=searchName, width=36, bd=0, fg="white", bg="black",height=2).grid(column=2, row=2, columnspan=2, pady=5)
        tk.Button(topFrame, text=f"搜尋低於此價格", command=searchPrice, width=36, bd=0, fg="white", bg="black",height=2).grid(column=4, row=2, columnspan=2, pady=5)
        tk.Button(topFrame, text=f"低於合理價", command=updateStockScreen_50, width=36, bd=0, fg="white", bg="black",height=2).grid(column=0, row=3, columnspan=2, pady=5)
        tk.Button(topFrame, text=f"低於便宜價", command=updateStockScreen_66, width=36, bd=0, fg="white", bg="black",height=2).grid(column=2, row=3, columnspan=2, pady=5)
        tk.Button(topFrame, text=f"低於超低價", command=updateStockScreen_99, width=36, bd=0, fg="white", bg="black",height=2).grid(column=4, row=3, columnspan=2, pady=5)
        self.updateStockScreen(10)

    def createCheckStockLabel(self, id):
        listStockInfo = GetData().getStockInfo(id)
        priceNow = float(Spider(id).getPriceNow())
        yieldNow = float(GetData().getLastDividend(id))
        autoUpdate = True
        print(listStockInfo)
        def updatePriceNow():
            print("autoUpdate:",autoUpdate)
            if autoUpdate == False:
                return
            priceNow = float(Spider(id).getPriceNow())
            boxPrice.configure(text=f"{Spider(id).getPriceNow()}")
            boxYield.configure(text="{}%".format(round(yieldNow/priceNow*1000)/100))
            # self.box.pack(padx=10, pady=10)
            self.after(60 * 1000, updatePriceNow)
        def backScotkList():
            topFrame.destroy()
            autoUpdate = False
            self.treeViewDividend.pack_forget()
            self.treeViewProfit.pack_forget()
            self.topFrame.pack()
            self.treeViewStock.pack()
        def gotoDividendList():
            buttonGotoDividend.configure(bg="blue")
            buttonGotoProfit.configure(bg="black")
            self.treeViewProfit.pack_forget()
            self.treeViewDividend.pack()
        def gotoProfitList():
            buttonGotoDividend.configure(bg="black")
            buttonGotoProfit.configure(bg="blue")
            self.treeViewDividend.pack_forget()
            self.treeViewProfit.pack()
        topFrame = tk.Frame(self)
        topFrame.pack()
        print(yieldNow)
        boxPrice = tk.Label(topFrame, text=f"{priceNow}", anchor="w",width=15)
        boxYield = tk.Label(topFrame, text="{}%".format(round(yieldNow/priceNow*1000)/100), anchor="w",width=15)
        tk.Label(topFrame, text=f"股號：", anchor="e",width=15).grid(column=0, row=0, pady=5)
        tk.Label(topFrame, text=f"{listStockInfo[0]}", anchor="w",width=15).grid(column=1, row=0, pady=5)
        tk.Label(topFrame, text=f"上市公司：", anchor="e",width=15).grid(column=2, row=0, pady=5)
        tk.Label(topFrame, text=f"{listStockInfo[1]}", anchor="w",width=15).grid(column=3, row=0, pady=5)
        tk.Label(topFrame, text=f"上市時間：", anchor="e",width=15).grid(column=4, row=0, pady=5)
        tk.Label(topFrame, text=f"{listStockInfo[3]}", anchor="w",width=15).grid(column=5, row=0, pady=5)
        tk.Label(topFrame, text=f"行業別：", anchor="e",width=15).grid(column=0, row=1, pady=5)
        tk.Label(topFrame, text=f"{listStockInfo[4]}", anchor="w",width=15).grid(column=1, row=1, pady=5)
        tk.Label(topFrame, text=f"股本：", anchor="e",width=15).grid(column=2, row=1, pady=5)
        tk.Label(topFrame, text='{:,}'.format(listStockInfo[5]), anchor="w",width=15).grid(column=3, row=1, pady=5)
        tk.Label(topFrame, text=f"董監持股比例：", anchor="e",width=15).grid(column=4, row=1, pady=5)
        tk.Label(topFrame, text=f"{listStockInfo[6]}%", anchor="w",width=15).grid(column=5, row=1, pady=5)
        tk.Label(topFrame, text=f"現在股價：", anchor="e",width=15).grid(column=0, row=2, pady=5)
        boxPrice.grid(column=1, row=2, pady=5)
        tk.Label(topFrame, text=f"殖利率：", anchor="e",width=15).grid(column=2, row=2, pady=5)
        boxYield.grid(column=3, row=2, pady=5)
        tk.Label(topFrame, text=f"最近收盤價：", anchor="e",width=15).grid(column=4, row=2, pady=5)
        tk.Label(topFrame, text=f"{listStockInfo[2]}", anchor="w",width=15).grid(column=5, row=2, pady=5)
        tk.Button(topFrame, text=f"返回上市公司列表",command=backScotkList,width=36,bd=0,fg="white",bg="black",height=2).grid(column=0, row=3,columnspan=2, pady=5)
        buttonGotoDividend = tk.Button(topFrame, text=f"檢視歷年收益及配息", command=gotoDividendList,width=36,bd=0,fg="white",bg="blue",height=2)
        buttonGotoDividend.grid(column=2, row=3,columnspan=2, pady=5)
        buttonGotoProfit = tk.Button(topFrame, text=f"檢視每季營業收益", command=gotoProfitList,width=36,bd=0,fg="white",bg="black",height=2)
        buttonGotoProfit.grid(column=4, row=3,columnspan=2, pady=5)
        self.createTreeViewDividend(id)
        self.createTreeViewProfit(id)
        updatePriceNow()

    def createTreeViewDividend(self, id):
        treeViewDividend = self.treeViewDividend
        treeViewDividend.heading('year',text='年份')
        treeViewDividend.heading('income', text='收益')
        treeViewDividend.heading('gross_profit', text='毛利')
        treeViewDividend.heading('gross_margin', text='毛利率')
        treeViewDividend.heading('EPS', text='每股盈餘')
        treeViewDividend.heading('cash_dividends', text='現金股利')
        treeViewDividend.heading('stock_dividends', text='股票股利')

        treeViewDividend.column('year',width=100, anchor=tkinter.CENTER)
        treeViewDividend.column('income',width=100, anchor=tkinter.E)
        treeViewDividend.column('gross_profit',width=100, anchor=tkinter.E)
        treeViewDividend.column('gross_margin',width=100, anchor=tkinter.E)
        treeViewDividend.column('EPS',width=100, anchor=tkinter.E)
        treeViewDividend.column('cash_dividends',width=150, anchor=tkinter.E)
        treeViewDividend.column('stock_dividends',width=150, anchor=tkinter.E)
        treeViewDividend.pack()
        self.updateDividendScreen(id)


    def updateDividendScreen(self,id):
        for i in self.treeViewDividend.get_children():
            self.treeViewDividend.delete(i)
        response = GetData().getListDividend(id)
        for item in response:
            item = list(item)
            grossMargin = '無資料' if item[1] == 0 else round(item[2] / item[1] * 10000)/100
            item[1] = '無資料' if item[1] == 0 else '{:,}'.format(item[1])
            item[2] = '無資料' if item[2] == 0 else '{:,}'.format(item[2])
            item.insert(3, grossMargin)
            item[4] = '無資料' if item[4] == 0 else round(item[4]*100) / 100
            self.treeViewDividend.insert('', 'end', values=item)

    def createTreeViewProfit(self, id):
        treeViewProfit = self.treeViewProfit
        treeViewProfit.heading('quarter',text='季度')
        treeViewProfit.heading('income', text='收益')
        treeViewProfit.heading('gross_profit', text='毛利')
        treeViewProfit.heading('gross_margin', text='毛利率')
        treeViewProfit.heading('EPS', text='每股盈餘')

        treeViewProfit.column('quarter',width=160, anchor=tkinter.CENTER)
        treeViewProfit.column('income',width=160, anchor=tkinter.E)
        treeViewProfit.column('gross_profit',width=160, anchor=tkinter.E)
        treeViewProfit.column('gross_margin',width=160, anchor=tkinter.E)
        treeViewProfit.column('EPS',width=160, anchor=tkinter.E)
        self.updateProfitScreen(id)

    def updateProfitScreen(self,id):
        for i in self.treeViewProfit.get_children():
            self.treeViewProfit.delete(i)
        response = GetData().getListProfit(id)
        for item in response:
            item = list(item)
            grossMargin = '無資料' if item[1] == 0 else round(item[2] / item[1] * 10000)/100
            item[1] = '無資料' if item[1] == 0 else '{:,}'.format(item[1])
            item[2] = '無資料' if item[2] == 0 else '{:,}'.format(item[2])
            item.insert(3, grossMargin)
            item[4] = '無資料' if item[4] == 0 else round(item[4]*100) / 100
            self.treeViewProfit.insert('', 'end', values=item)

    def createTreeViewStock(self):
        treeViewStock = self.treeViewStock
        treeViewStock.heading('id',text='股號')
        treeViewStock.heading('name', text='股名')
        treeViewStock.heading('d_yield', text='現金殖利率(%)')
        treeViewStock.heading('price', text='最近收盤價')
        treeViewStock.heading('classification', text='產類別')
        treeViewStock.heading('5y_EPS', text='五年平均\n每股盈餘')
        treeViewStock.heading('5y_yield', text='五年平均\n現金殖利率')
        treeViewStock.heading('5y_yield2', text='五年平均\n股票股利')
        treeViewStock.heading('judge', text='價位')

        treeViewStock.column('id',width=75 , anchor=tkinter.CENTER )
        treeViewStock.column('name',width=75, anchor=tkinter.CENTER)
        treeViewStock.column('d_yield',width=75, anchor=tkinter.E)
        treeViewStock.column('price', width=100, anchor=tkinter.E)
        treeViewStock.column('classification', width=100, anchor=tkinter.CENTER)
        treeViewStock.column('5y_EPS', width=100, anchor=tkinter.E)
        treeViewStock.column('5y_yield', width=100, anchor=tkinter.E)
        treeViewStock.column('5y_yield2', width=100, anchor=tkinter.E)
        treeViewStock.column('judge', width=75, anchor=tkinter.CENTER)
        treeViewStock.pack()

    def checkStock(self,event):
        for item in self.treeViewStock.selection():
            item_text = self.treeViewStock.item(item, "values")
            print(item_text[0])
            if item_text[0] != "股號":
                self.treeViewStock.pack_forget()
                self.topFrame.pack_forget()
                self.createCheckStockLabel(item_text[0])
            return

    def updateStockScreen(self,key="d_yield",link=">=",value=5):
        for i in self.treeViewStock.get_children():
            self.treeViewStock.delete(i)
        response = GetData().getListStock(key,link,value)
        for item in response:
            item = list(item)
            #print("yyyy",item[0])
            r = GetData().getSumInfo(item[0])
            x = [0,0,0]
            for i in r:
                #print(i)
                #print("VVVVV",x[0],x[1],x[2])
                x[0] += i[0]
                x[1] += i[1]
                x[2] += i[2]

            x[0] = x[0] / 5
            x[1] = x[1] / 5
            x[2] = x[2] / 5
            item.append(round(x[0]*100)/100)
            if x[1] != 0 and item[4] != 0:
                item.append(round(x[1]*10000/item[4])/100)
            else:
                item.append(0)
            item.append(round(x[2]*100)/100)
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