from ctypes.wintypes import INT
import sqlite3
import os
import sqlalchemy
import CryptUtil
from sqlalchemy.orm import Session
from sqlalchemy import Table, Column, Integer, String, MetaData

engine = sqlalchemy.create_engine('sqlite:///./database/bank.db')
connection = engine.connect()
meta = sqlalchemy.MetaData()

#User DataTable
userTable = Table(
'USER', meta, 
Column('id', Integer, primary_key = True,autoincrement=True), 
Column('user_name', String), 
Column('balance', Integer), 
Column('password_hash', String), 
)

def createNewDatabase():
    if os.path.isfile("./database/bank.db"):
        os.remove("./database/bank.db")        
    SQLQuery:str
    with open("./database/schema","r", encoding = 'utf-8') as f:
        SQLQuery=f.read()
    conn=None
    conn = sqlite3.connect("./database/bank.db")
    c = conn.cursor()
    c.execute(SQLQuery)
    conn.close()

#https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_quick_guide.htm
def insertUser(user_name_i:str,balance_i:int,password_hash_i:str):
    ins = userTable.insert().values(user_name=user_name_i,balance=balance_i,password_hash=password_hash_i)
    conn = engine.connect()
    conn.execute(ins)

def creatExampleUser():
    insertUser("Alice",100,CryptUtil.bytesToBase64String(CryptUtil.StringSHA256("abc")))
    insertUser("Bob",100,CryptUtil.bytesToBase64String(CryptUtil.StringSHA256("def")))

def getPasswordHash(userNme:str=""):
    s=userTable.select().where(userTable.c.user_name==userNme)
    conn = engine.connect()
    results = conn.execute(s)
    returnResult=None
    for result in results:
        returnResult=result[3]
    return returnResult

def getUserID(userNme:str=""):
    s=userTable.select().where(userTable.c.user_name==userNme)
    conn = engine.connect()
    results = conn.execute(s)
    returnResult=None
    for result in results:
        returnResult=result[0]
    return returnResult