import requests
import json


state = requests.get(firebase_url)
firebase_url = "https://blink-8bae2.firebaseio.com/openCV.json"

# set sleeping and status in payload
payload = {"sleeping": "true", "status": "bob"}
headers = {"Content-Type": "application/json"}



# PUT
response = requests.put(firebase_url, data=json.dumps(payload), headers=headers)


