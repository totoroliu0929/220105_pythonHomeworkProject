from models import GetData
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
        self.updateData()

    def updateData(self):
        now = datetime.now()
        nowString = now.strftime("%Y-%m-%d %H:%M:%S")
        self.mainLabelFrame.updateScreen()
        self.mainLabelFrame.configure(text=nowString)
        self.after(60 * 1000, self.updateData)


class MainLabelFrame(tk.LabelFrame):
    def __init__(self, *args , **kwargs):
        super().__init__(*args, **kwargs)
        topFrame = tk.Frame(self,background='gray')
        tk.Label(topFrame, text="正常租借站點", font=("arial", 20),background='gray',fg="white").pack(padx=10,pady=10)
        #normal_count = dataSource.get_count_of_normal()
        tk.Label(topFrame, text=f"數量:",background='gray',fg='#ffffff', font=("arial",20)).pack(padx=10,pady=10)
        #topFrame.pack(pady=20)
        treeView = ttk.Treeview(self,columns=('id','name','d_yield','price','10y_EPS','10y_yield','10y_yield2','judge'),show="headings")
        self.treeView = treeView
        treeView.heading('id',text='股號')
        treeView.heading('name', text='股名')
        treeView.heading('d_yield', text='現金殖利率')
        treeView.heading('price', text='最近收盤價')
        treeView.heading('10y_EPS', text='十年平均每股盈餘')
        treeView.heading('10y_yield', text='十年平均現金殖利率')
        treeView.heading('10y_yield2', text='十年平均股票股利')
        treeView.heading('judge', text='價位')

        treeView.column('id',width=100)
        treeView.column('name',width=100)
        treeView.column('d_yield',width=100)
        treeView.column('price', width=100)
        treeView.column('10y_EPS', width=100)
        treeView.column('10y_yield', width=100)
        treeView.column('10y_yield2', width=100)
        treeView.column('judge', width=100)
        treeView.pack()

    def checkStock(self,event):
        for item in self.treeView.selection():
            item_text = self.treeView.item(item, "values")
            print(item_text[0])
        self.treeView.pack_forget()
        return

    def updateScreen(self):
        for i in self.treeView.get_children():
            self.treeView.delete(i)
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
            item.append(round(x[1]*10000/item[3])/100)
            item.append(x[2])
            y = ""
            if item[2]>=10:
                y = "超低"
            elif item[2] >= 6.6:
                y = "便宜"
            elif item[2] >= 5:
                y = "合理"
            item.append(y)
            self.treeView.insert('', 'end', values=item)
            self.treeView.bind("<ButtonRelease-1>",self.checkStock)


if __name__=="__main__":
    window = Window()
    window.title("存股輔助系統")
    window.mainloop()