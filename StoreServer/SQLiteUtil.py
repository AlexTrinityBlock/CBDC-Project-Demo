from ctypes.wintypes import INT
import sqlite3
import os
import sqlalchemy
import CryptUtil
from sqlalchemy.orm import Session
from sqlalchemy import Table, Column, Integer, String, MetaData

engine = sqlalchemy.create_engine('sqlite:///./database/store.db')
connection = engine.connect()
meta = sqlalchemy.MetaData()

#User DataTable
storeWalletTable = Table(
'STOREWALLET', meta, 
Column('id', Integer, primary_key = True,autoincrement=True), 
Column('hidden_user_info', String), 
Column('digital_currency', String)
)

def createNewDatabase():
    if os.path.isfile("./database/store.db"):
        os.remove("./database/store.db")        
    SQLQuery:str
    with open("./database/schema","r", encoding = 'utf-8') as f:
        SQLQuery=f.read()
    conn=None
    conn = sqlite3.connect("./database/store.db")
    c = conn.cursor()
    c.execute(SQLQuery)
    conn.close()

#https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_quick_guide.htm
def insertTrade(hidden_user_info_i:str,digital_currency_i:str):
    ins = storeWalletTable.insert().values(hidden_user_info=hidden_user_info_i,digital_currency=digital_currency_i)
    conn = engine.connect()
    conn.execute(ins)