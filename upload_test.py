import requests
url = 'https://thc-lab.net/art.html'
url = 'http://127.0.0.1:5000/art.html'
files = {'xxx.jpg': open('xxx.jpg', 'rb')}



payload = {
    'code':'fuck you you fucking fuck',
    'url':'https://oaidalleapiprodscus.blob.core.windows.net/private/org-mTzTvHawi8YV97uIRhF5YlF8/user-ho8zfzMJbxmDNV5eWY0rEiC1/img-M4HIdPOaiSSrAx3zbbj6Moxo.png?st=2022-11-30T16%3A43%3A23Z&se=2022-11-30T18%3A43%3A23Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2022-11-29T21%3A06%3A46Z&ske=2022-11-30T21%3A06%3A46Z&sks=b&skv=2021-08-06&sig=PiAm76PdXCKm3vVRv5X25XzV5pmY4Jkc33FLiDgna%2Bw%3D',
    'filename': 'THC_Cavepainting_11302022.jpg'
}

r = requests.post(url, data=payload)
print(r.text)
