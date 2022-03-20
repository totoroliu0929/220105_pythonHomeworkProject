from models import Spider, UpdateData, GetData
print( UpdateData())

import sqlite3
from sqlite3 import Error as sqlite3Error

dbFile = 'yield.db'


def createConnection():
    conn = None
    try:
        conn = sqlite3.connect(dbFile)
    except sqlite3Error as e:
        print("sqlite連線錯誤")
        print(e)
        return
    return conn

def getSumInfo(id):
    conn = createConnection()
    sql = '''
        SELECT EPS,cash_dividends,stock_dividends
        FROM dividend
        WHERE payment = 1 AND stock_id = '{}'
        limit 0, 10
        '''.format(id)
    rows = list()
    with conn:
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            print(rows)
        except sqlite3Error as e:
            print(e)
    return rows

print(getSumInfo("2330"))