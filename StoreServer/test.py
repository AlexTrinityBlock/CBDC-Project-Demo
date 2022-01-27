from urllib import response
import requests
import json

#Login Test
# responseObeject = requests.post('http://127.0.0.1:5000/login', data={'user_name': 'Alice','user_password':'abc'})
# responseJSON=json.loads(responseObeject.text)
# if responseJSON["status"] =="True":print("Normal Login OK")
# else:print("Normal Login Error")
# responseObeject=None

requestsObeject = requests.Session()
responseText=requestsObeject.get('http://127.0.0.1:5000/get-session').text
print(responseText)
responseText=requestsObeject.get('http://127.0.0.1:5000/check-session').text
print(responseText)