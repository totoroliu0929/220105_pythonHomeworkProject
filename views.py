from models import GetData
import tkinter as tk
from tkinter import ttk
#from datetime import datetime

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


class MainLabelFrame(tk.LabelFrame):
    def __init__(self, *args , **kwargs):
        super().__init__(*args, **kwargs)
        topFrame = tk.Frame(self,background='gray')
        tk.Label(topFrame, text="正常租借站點", font=("arial", 20),background='gray',fg="white").pack(padx=10,pady=10)
        #normal_count = dataSource.get_count_of_normal()
        tk.Label(topFrame, text=f"數量:",background='gray',fg='#ffffff', font=("arial",20)).pack(padx=10,pady=10)
        topFrame.pack(pady=20)
        treeView = ttk.Treeview(self,columns=('id','name','d_yield','price','10y_yield','10y_EPS'),show="headings")
        self.treeView = treeView
        treeView.heading('id',text='股號')
        treeView.heading('name', text='股名')
        treeView.heading('d_yield', text='現金殖利率')
        treeView.heading('price', text='最近收盤價')
        treeView.heading('10y_yield', text='十年現金殖利率')
        treeView.heading('10y_EPS', text='十年每股盈餘')

        treeView.column('id',width=50)
        treeView.column('name',width=50)
        treeView.column('d_yield',width=50)
        treeView.column('price', width=50)
        treeView.column('10y_yield', width=50)
        treeView.column('10y_EPS',width=50)
        treeView.pack()

        response = GetData().getListStock()
        for item in response:
            print("yyyy",item[0])


if __name__=="__main__":
    window = Window()
    window.title("台北市youbike及時監測資料")
    window.mainloop()