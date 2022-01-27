# Scripts\activate.bat
# flask run --host=0.0.0.0
# pip install -r requirements.txt 
import flask
import SQLiteUtil
import CryptUtil
import AccountUtil
import CurrencyUtil
import json
import os
from flask import render_template,Flask,session,request
from datetime import timedelta

app = flask.Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/public-key/user/withdraw',methods=['GET'])
def transportPubblicKey():
    result:dict
    try:
        publicKeyBase64=CryptUtil.bytesToBase64String(CryptUtil.readBytes("PublicKey.pem"))
        result={
            "PublicKey":publicKeyBase64
        }
    except:
        result="[server]Public Key no found,try to use CryptUtil.RSAKeyPairFilesGenerator()"
    return json.dumps(result)
    
@app.route('/get-currency',methods=['POST'])
def getCurrency():
    result=dict()
    try:
        cipher_user_input:str=request.values['cipher_user_input']
        user_rsa_public_key=CryptUtil.Base64StringToBytes(request.values['user_rsa_public_key'])
        plain_user_input=(CryptUtil.RSAdecrypto(CryptUtil.Base64StringToBytes(cipher_user_input),CryptUtil.readBytes("PrivateKey.pem"))).decode("utf-8")
        user_input_json=json.loads(plain_user_input)
        if AccountUtil.checkUserPassword(user_input_json["user_name"],user_input_json["user_password"]):
            result={
                "Status":"Success"            
            }
        else:
            result={
                "Status":"Fail"            
            }

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
