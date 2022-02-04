# Scripts\activate.bat
# flask run --port 7070
# pip install -r requirements.txt 
from unittest import result
import flask
import SQLiteUtil
import uuid
import json
import CryptUtil
import VerifyUtil
import os
from flask import render_template,Flask,session,request
from datetime import timedelta

app = flask.Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
app.config['SECRET_KEY'] = os.urandom(24)

publicKeyBase64=CryptUtil.bytesToBase64String(CryptUtil.readBytes("PublicKey.pem"))
privateKeyBase64=CryptUtil.bytesToBase64String(CryptUtil.readBytes("PrivateKey.pem"))

# @app.route('/')
# def API1():
#     result:dict
#     try:
#         result={
#             "Key":"value"
#         }
#     except Exception as e:
#         result="[server]"+e
#     return json.dumps(result)

# @app.route('/check-session')
# def API2():
#     result:dict
#     try:
#         if  session["test"]==1 :
#             result={
#                 "status":"OK"
#             }
#         else :
#             result={
#                 "status":"Not OK"
#             }
#     except Exception as e:
#         result={
#             "status":"Not OK",
#         }
#     return json.dumps(result)

# @app.route('/get-session')
# def API3():
#     result:dict
#     try:
#         session["test"]=1
#     except Exception as e:
#         result="[server]"+str(e)
#         return result
#     return "You get session"

@app.route('/store/public-key/',methods=['GET'])
def getStorePublicKey():
    result={
        "PublicKey":CryptUtil.bytesToBase64String(CryptUtil.readBytes("PublicKey.pem"))
    }
    return result

@app.route('/start-transaction/get-binary-string',methods=['GET'])
def StartTransaction():
    result:dict()
    session["RandomBinaryString"]=None
    session["ClientStart"]=None
    session["ClientStart"]="True"
    session["RandomBinaryString"]=VerifyUtil.randomBinaryString(10)
    return session["RandomBinaryString"]

@app.route('/get-currency',methods=['GET'])
def getCurrency():
    if session.get("RandomBinaryString")==None:return "Please get your session and Random Binary String First"
    return "OK"


if __name__ == '__main__':
    app.run()
