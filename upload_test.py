import requests
url = 'https://thc-lab.net/art.html'
files = {'test.jpg': open('boat.jpg','rb')}
r = requests.post(url, files=files)
print(r.text)