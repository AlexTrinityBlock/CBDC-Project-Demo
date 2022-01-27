import requests
import json
import CryptUtil

#Login Test
# responseObeject = requests.post('http://127.0.0.1:5000/login', data={'user_name': 'Alice','user_password':'abc'})
# responseJSON=json.loads(responseObeject.text)
# if responseJSON["status"] =="True":print("Normal Login OK")
# else:print("Normal Login Error")
# responseObeject=None

# responseObeject = requests.post('http://127.0.0.1:5000/login', data={'user_name': 'Alice','user_password':'def'})
# responseJSON=json.loads(responseObeject.text)
# if responseJSON["status"] =="False":print("Fail Login OK")
# else:print("Fail Login Error")
# responseObeject=None

# responseObeject = requests.post('http://127.0.0.1:5000/login', data={'user_name': '','user_password':''})
# responseJSON=json.loads(responseObeject.text)
# if responseJSON["status"] =="False":print("NULL Login OK")
# else:print("NULL Login Error")
# responseObeject=None
#Login Test End

#Get Public key

#User Key Pair
keyPair=CryptUtil.RSAKeyPair()
UserPublicKey=keyPair["PublicKey"]
UserPrivateKey=keyPair["PrivateKey"]


#User get bank's public key
requestSessionObject=requests.Session()
responseObeject = requestSessionObject.get('http://127.0.0.1:5000/public-key/user/withdraw')
responseJSON=json.loads(responseObeject.text)
serverPublicKey= CryptUtil.Base64StringToBytes(responseJSON["PublicKey"])

#User send to bank for withdraw
user_input={
    "user_name":"Alice",
    "user_password":"abc",
    # "withdrawal_number":"1",
}
user_input_bytes=bytes(json.dumps(user_input),"utf-8")
CipherText=CryptUtil.RSAencrypto(user_input_bytes,serverPublicKey)
CipherTextB64=CryptUtil.bytesToBase64String(CipherText)
responseText=requestSessionObject.post('http://127.0.0.1:5000/get-currency',data={'cipher_user_input': CipherTextB64,'user_rsa_public_key':CryptUtil.bytesToBase64String(UserPublicKey)}).text
print(responseText)