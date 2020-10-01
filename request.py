import requests

url = 'http://localhost:5000/predict_api'
r = requests.post(url,json={'BP':80, 'Sugar':65, 'oxvalue':55})

print(r.json())