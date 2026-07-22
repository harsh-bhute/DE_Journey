# Searched Flipkart to see their API calls 
# first buisness releted URL its a POST request ,status code is 200 meaning its OK
# Also theres another API 'state' which has same request and also with a reponse json 
# some requests doesnt have this general information



import requests 

response = requests.get("https://jsonplaceholder.typicode.com/users")

print(response.status_code)
print(type(response.json()))
print(response.json())



for i in response.json():

    print(f"Name:{i['name']} | Email:{i['email']}")