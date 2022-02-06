# Scripts\activate.bat
# flask run --host=0.0.0.0
#flask run --port 8080
# pip install -r requirements.txt 
from locale import currency
import flask
import CryptUtil
import AccountUtil
import CurrencyUtil
import SQLiteUtil
import VerifyUtil
import json
import os
from flask import render_template,Flask,session,request
from datetime import timedelta
from flask import render_template

app = flask.Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/',methods=['GET'])
def homePage():
    #User Info
    UsersInfo:list=SQLiteUtil.getAllUserInfoForFrontEnd()
    CurrencysInfo:list=SQLiteUtil.getCurrencyInfoForFrontEnd()
    DoubleSpendingUsersInfo:list=SQLiteUtil.getDoubleSpendingUserInfoForFrontEnd()
    return render_template('index.html',UsersInfo=UsersInfo,CurrencysInfo=CurrencysInfo,DoubleSpendingUsersInfo=DoubleSpendingUsersInfo) 

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
    bankPrivateKey:bytes=CryptUtil.readBytes("PrivateKey.pem")
    
    # try:
    cipher_user_input:str=request.values['cipher_user_input']
    user_rsa_public_key=CryptUtil.Base64StringToBytes(request.values['user_rsa_public_key'])
    plain_user_input=(CryptUtil.RSAdecrypto(CryptUtil.Base64StringToBytes(cipher_user_input),bankPrivateKey)).decode("utf-8")
    user_input_json=json.loads(plain_user_input)
    user_name=user_input_json["user_name"]
    if AccountUtil.checkUserPassword(user_name,user_input_json["user_password"]):
        currencyList=list()
        cipherCurrencyList=list()

        for i in range(user_input_json["withdrawal_number"]):
            currencyList.append(CurrencyUtil.issueNewCurrency())
            SQLiteUtil.decreaseBalanceByUserName(user_name)

        for plainCurrency in currencyList:
            cipherCurrency:bytes=CryptUtil.RSAencrypto(bytes(plainCurrency,"utf-8"),user_rsa_public_key)
            CurrencyBase64=CryptUtil.bytesToBase64String(cipherCurrency)
            CurrencyBase64Signature=CryptUtil.RSASignature(CurrencyBase64,bankPrivateKey)
            cipherCurrencyElement={
                "Currency":CurrencyBase64,
                "BankSignature":CurrencyBase64Signature
            }
            cipherCurrencyList.append(cipherCurrencyElement)

        result={
            "Status":"Success",
            "cipher_currency": cipherCurrencyList     
        }
    else:
        result={
            "Status":"Fail"            
        }
    return json.dumps(result)

@app.route('/deposit',methods=['POST'])
def deposit():
    bankPrivateKey=CryptUtil.bytesToBase64String(CryptUtil.readBytes("PrivateKey.pem"))
    DepositJson:dict=json.loads(request.values['Deposit'])
    HiddenUserInfoList=DepositJson["hidden_user_info"]
    Currency=CryptUtil.Base64RSADecrypt( DepositJson["CipherCurrency"],bankPrivateKey)
    #Check if it's valid coin
    if VerifyUtil.checkIfCurrencyDeposited(Currency) and  VerifyUtil.checkCurrencyIsReal(Currency):
        print("Coin: ",Currency,"is Deposited")
        double_spendiner=VerifyUtil.findUserInfoFromHiddenInfoByCurrency(Currency,HiddenUserInfoList)
        SQLiteUtil.setDoubleSpenderbyUserID(double_spendiner)
        return "Fail"
    else:
        SQLiteUtil.setCurrencyDeposited(Currency,HiddenUserInfoList)
        return "Success"

if __name__ == '__main__':
    app.run()

