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

@app.route('/public-key')
def transportPBK():
    result:dict
    try:
        publicKeyBase64=CryptUtil.bytesToBase64String(CryptUtil.readBytes("PrivateKey.pem"))
        result={
            "PublicKey":publicKeyBase64
        }
    except:
        result="[server]Public Key no found,try to use CryptUtil.RSAKeyPairFilesGenerator()"
    return json.dumps(result)

@app.route('/login',methods=['POST'])
def login():
    result=dict()
    try:
        #
        userName:str=request.values['user_name']
        userInputPassword=request.values['user_password']
        userPasswordHash=SQLiteUtil.getPasswordHash(userName)
        userInputPasswordHash=CryptUtil.bytesToBase64String(CryptUtil.StringSHA256(userInputPassword))
        if userPasswordHash==userInputPasswordHash and userInputPassword!="" :
            session["user_id"]=SQLiteUtil.getUserID(userName)
            result={
                "status":"True",
                "session":session["user_id"]
            }
        else:
            result={
                "status":"False",
            }
        #
    except Exception as e:
        result="[server] Error"+str(e)
    return result



# @app.route('/TakeMoney')
# def takemoney():
#     money = uuid.uuid4()
#     money = str(money)

#     PIK = None
#     with open("private.pem", "rb") as f:
#         PIK = f.read()
#     key = RSA.importKey(PIK)
#     cipher = PKCS1_OAEP.new(key).encrypt(bytes(money, 'utf-8'))
#     cipher = bytesToBase64String(cipher)

#     str1 = {
#         'money' : money, 
#         'cipher' : cipher
#         }
#     str1 = json.dumps(str1)
#     return str1

if __name__ == '__main__':
    # app.run()
    SQLiteUtil.createNewDatabase()
    SQLiteUtil.creatExampleUser()
    print(SQLiteUtil.getPasswordHash("Alice"))
    print(CryptUtil.bytesToBase64String(CryptUtil.StringSHA256("abc")))
