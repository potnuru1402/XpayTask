import requests

url = "http://127.0.0.1:6451/users/29"

r = requests.get(url)
print(r.text)