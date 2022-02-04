import requests
import json
import CryptUtil
import SQLiteUtil

#Bank URL
BankPublicKeyURL:str='http://127.0.0.1:8080/public-key/user/withdraw'
BankGetCurrencyURL:str='http://127.0.0.1:8080/get-currency'

#Currency List
currencyList=list()

#UserID
user_name="Alice"
user_uuid="30a1bf87-b0e1-4921-a0b8-8c602af1f391"

#User Key Pair
keyPair=CryptUtil.RSAKeyPair()
UserPublicKey=keyPair["PublicKey"]
UserPrivateKey=keyPair["PrivateKey"]


#User get bank's public key
requestSessionObject=requests.Session()
responseObeject = requestSessionObject.get(BankPublicKeyURL)
responseJSON=json.loads(responseObeject.text)
serverPublicKey= CryptUtil.Base64StringToBytes(responseJSON["PublicKey"])


def GetCurrency():
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

if __name__ == '__main__':
    GetCurrency()