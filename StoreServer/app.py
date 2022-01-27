# Scripts\activate.bat
# flask run --host=0.0.0.0
# pip install -r requirements.txt 
import flask
import SQLiteUtil
import uuid
import json
import CryptUtil
import os
from flask import render_template,Flask,session,request
from datetime import timedelta

app = flask.Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def API1():
    result:dict
    try:
        result={
            "Key":"value"
        }
    except Exception as e:
        result="[server]"+e
    return json.dumps(result)

@app.route('/check-session')
def API2():
    result:dict
    try:
        if  session["test"]==1 :
            result={
                "status":"OK"
            }
        else :
            result={
                "status":"Not OK"
            }
    except Exception as e:
        result={
            "status":"Not OK",
        }
    return json.dumps(result)

@app.route('/get-session')
def API3():
    result:dict
    try:
        session["test"]=1
    except Exception as e:
        result="[server]"+str(e)
        return result
    return "You get session"

if __name__ == '__main__':
    SQLiteUtil.createNewDatabase()
    SQLiteUtil.insertTrade("AAA","BBB")
