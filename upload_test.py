import requests
url = 'https://thc-lab.net/upload'
files = {'xxx.jpg': open('xxx.jpg', 'rb')}
r = requests.post(url, files=files)
print(r.text)