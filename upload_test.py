import requests
url='https://thc-lab.net/upload'
files={'files': open('app/static/uploads/boat.jpg','rb')}
values={'upload_file' : 'suckittest.jpg'}
r=requests.post(url,files=files)
