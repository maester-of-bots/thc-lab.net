from flask import Blueprint, request, render_template, redirect, url_for, send_file
import requests

import socket

from app.minecraft import blueprint

mc = Blueprint('mc', __name__)




def get_ips():
    data1 = socket.gethostbyname_ex("thc-lab.net")
    data2 = socket.gethostbyname_ex("home.thc-lab.net")
    total = list(data1+data2)
    ips = []

    for thing in total:
        if thing == []:
            check = "thc"
        elif type(thing) == list:
            check = thing[0]
        elif type(thing) == str:
            check = thing
        else:
            check = "thc"
        if "thc" in check:
            pass
        else:
            ips.append(check)


    return ips

def secCheck(address):
    if address in get_ips():
        return True
    else:
        return False



@blueprint.route('/minecraft.html', methods=['POST'])
def mc_ost():

    data = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    if secCheck(data):
        text = request.data.decode('utf-8')
        print(text)
        url = "https://discord.com/api/webhooks/1167186135949254756/IqxTtHPZhPxR_hHG-ZRrxP0SbjuMWo_92NUY2el_yc6U28Y6DVOLaRPhTZulZ2f3EsK9"

        data = {"content": "message content", "username": "custom username", "embeds": [
            {
                "description": text,
                "title": "embed title"
            }
        ]}
        result = requests.post(url, json=data)

