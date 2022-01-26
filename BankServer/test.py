from urllib import response
import requests
import json

#Login Test
responseObeject = requests.post('http://127.0.0.1:5000/login', data={'user_name': 'Alice','user_password':'abc'})
responseJSON=json.loads(responseObeject.text)
if responseJSON["status"] =="True":print("Normal Login OK")
else:print("Normal Login Error")
responseObeject=None

responseObeject = requests.post('http://127.0.0.1:5000/login', data={'user_name': 'Alice','user_password':'def'})
responseJSON=json.loads(responseObeject.text)
if responseJSON["status"] =="False":print("Fail Login OK")
else:print("Fail Login Error")
responseObeject=None

responseObeject = requests.post('http://127.0.0.1:5000/login', data={'user_name': '','user_password':''})
responseJSON=json.loads(responseObeject.text)
if responseJSON["status"] =="False":print("NULL Login OK")
else:print("NULL Login Error")
responseObeject=None

#Login Test End
