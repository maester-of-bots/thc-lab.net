import requests
import json


class card:
    def __init__(self,data):
        self.raw = data
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.desc = data['desc']
        self.card_images = data['card_images']
        if self.type == "Normal Monster" or self.type == "Effect Monster" or self.type == "Flip Effect Monster":
            self.atk = data['atk']
            self.defens = data['def']
            self.race = data['race']
            self.attribute = data['attribute']
    def getInfo(self):
        if "Monster" in self.type:
            response = "{} - {}<br/>Attack: {}<br/>Defense: {}<br/>Description: {}<br/><br/>{}".format(self.name,self.type,self.atk,self.defens,self.desc,self.card_images[0]['image_url'])
        else:
            response = "{} - {}<br/>Description: {}<br/><br/><a href={}>Image</a>".format(self.name,self.type,self.desc,self.card_images[0]['image_url'])

        return response

def getAllCards():
    data = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php')
    raw = data.text.encode()
    allCards_raw = json.loads(raw.decode('utf-8'))['data']
    allCards = []
    for temp in allCards_raw:
        newCard = card(temp)
        allCards.append(newCard)
    return allCards




