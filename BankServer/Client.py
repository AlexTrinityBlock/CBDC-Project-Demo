from unittest import result
import requests
import json
import CryptUtil
import SQLiteUtil
import string    
import random

#Bank URL
BankPublicKeyURL:str='http://127.0.0.1:8080/public-key/user/withdraw'
BankGetCurrencyURL:str='http://127.0.0.1:8080/get-currency'

#Store URL
StorePublicKey="http://127.0.0.1:7070/store/public-key/"
StoreStartTransactionURL="http://127.0.0.1:7070/start-transaction/get-binary-string"


#Currency List
currencyList=list()

#UserID
user_name="Alice"
user_uuid="30a1bf87-b0e1-4921-a0b8-8c602af1f391"

#User Key Pair
keyPair=CryptUtil.RSAKeyPair()
UserPublicKey=keyPair["PublicKey"]
UserPrivateKey=keyPair["PrivateKey"]

def randomString(S):
    return  ''.join(random.choices(string.ascii_letters + string.digits, k = S))

def StringXOR(String1:str,String2:str):
    bytes1=String1.encode("utf-8")
    bytes2=String2.encode("utf-8")
    bytesXORed=bytes(a ^ b for a, b in zip(bytes1, bytes2))
    return CryptUtil.bytesToBase64String(bytesXORed)

def GetCurrency():
    #User get bank's public key
    requestSessionObject=requests.Session()
    responseObeject = requestSessionObject.get(BankPublicKeyURL)
    responseJSON=json.loads(responseObeject.text)
    serverPublicKey= CryptUtil.Base64StringToBytes(responseJSON["PublicKey"])
    #User send to bank for withdraw
    user_input={
        "user_name":"Alice",
        "user_password":"abc",
        "withdrawal_number":3,
    }
    user_input_bytes=bytes(json.dumps(user_input),"utf-8")
    CipherText=CryptUtil.RSAencrypto(user_input_bytes,serverPublicKey)
    CipherTextB64=CryptUtil.bytesToBase64String(CipherText)
    responseText=requestSessionObject.post(BankGetCurrencyURL,data={'cipher_user_input': CipherTextB64,'user_rsa_public_key':CryptUtil.bytesToBase64String(UserPublicKey)}).text

    #User decrypt bank response
    BanReturnCurrencyJson = json.loads(responseText)
    cipherCurrencyList=BanReturnCurrencyJson["cipher_currency"]

    for currencyAndSigNature in cipherCurrencyList:
        currency=CryptUtil.Base64RSADecrypt(currencyAndSigNature["Currency"],CryptUtil.bytesToBase64String(UserPrivateKey))
        currencyList.append({"Currency":currency,"BankSignature":currencyAndSigNature["BankSignature"]})

    print("===============Get Currency===============\n",json.dumps(currencyList, indent=4, sort_keys=True),"\n===================================\n")

#Send to Store
def SendToStroe():
    #init
    serverPublicKey=bytes()
    binaryString = str()
    randomStrings=[]

    #init random number
    for i in range(10):
        randomStrings.append(randomString(36))

    #User get store's public key
    requestSessionObject=requests.Session()
    responseObeject = requestSessionObject.get(StorePublicKey)
    responseJSON=json.loads(responseObeject.text)
    serverPublicKey= CryptUtil.Base64StringToBytes(responseJSON["PublicKey"])

    #Get binary String
    responseObeject=requestSessionObject.get(StoreStartTransactionURL)
    binaryString=responseObeject.text

    #XOR  follow Binary String to XOR UserID with Random Value
    resultList=list()
    counter=0
    for binaryChart in binaryString:
        if(binaryChart=="0"):
            resultList.append(randomStrings[counter])
        else:
            resultList.append(StringXOR(randomStrings[counter],user_uuid))
        counter+=1

    #Return Hidden user info to store
    result={
        ""
    }



    
    

    



if __name__ == '__main__':
    # GetCurrency()
    SendToStroe()
    # print(randomString(36))
    # print(StringXOR(randomString(36),randomString(36)))