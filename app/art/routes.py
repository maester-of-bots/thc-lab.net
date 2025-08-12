from app.art.variations import *

from flask import Blueprint, request, render_template, redirect, url_for
import requests

import socket

from app.art import blueprint

art = Blueprint('art', __name__)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def secCheck(address):
    print(address)
    data1 = socket.gethostbyname_ex("thc-lab.net")[2][0]
    data2 = socket.gethostbyname_ex("home.thc-lab.net")[2][0]
    total = [data1, data2]
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

        if address in ips:
            return True
        else:
            return False


@blueprint.route('/art.html', methods=['POST'])
def art_post():
    result = request.form

    data = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    if secCheck(data) and result['code'] == 'Yesbecausethisissecure101$':

        url = result['url']

        subdir = result['subdir']

        name = result['filename']

        if subdir == 'None':
            path = f'app/static/shared/all/{name}'
            newpath = f'https://thc-lab.net/static/shared/all/{name}'
        else:
            path = f'app/static/shared/{subdir}/{name}'
            newpath = f'https://thc-lab.net/static/shared/{subdir}/{name}'

        data = requests.get(url)

        with open(path,'wb') as image:
            image.write(data.content)

        return newpath

    else:
        print(result['code'])
        return result['code']#"Hey, you're not THC!"


# curl -v --unix-socket /var/www/thc-lab.net/main.sock http://localhost/variation.html -d 'code=fuck you you fucking fuck&url=https://www.telegraph.co.uk/content/dam/briefs/2025/07/22/TELEMMGLPICT000433194960_17531961502390_trans_NvBQzQNjv4Bq8VAndPZ2Bz0AY_iRYVPZ5P4Xpit_DMGvdp2n7FDd82k.jpeg?imwidth=1280'


@blueprint.route('/variation.html', methods=['POST'])
def variation():

    result = request.form

    print("Got a request.")

    data = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    print("Grabbed the data.")

    print(data)

    if secCheck(data) and result['code'] == 'fuck you you fucking fuck':

        print("We can respond.")

        AI = oldOpenAI()

        new_urls = AI.variation(result['url'])
        print(new_urls)

        return "\n".join(new_urls)

    elif not secCheck(data):

        print("SecCheck failed.")
        return "Bad IP."

    else:
        print("Bad Peen.")
        return "Bad peen!"

@blueprint.route('static/uploads/backgrounds/<filename>')
def display_background(filename):
    dirname = 'shared/backgrounds/'
    return redirect(url_for('static', filename=dirname + filename), code=301)

'''
@blueprint.route('static/uploads/backgrounds/<filename>')
def display_background(filename):
    dirname = 'shared/backgrounds/'
    return redirect(url_for('static', filename=dirname + filename), code=301)
'''

@blueprint.route('static/uploads/<filename>')
def old_uploads(filename):
    if "Variation" in filename:
        dirname = "shared/variations"
    else:
        dirname = "shared/all/"

    return redirect(url_for('static', filename=dirname + filename), code=301)

@blueprint.route('/display/<filename>')
def display_image(filename):
    if 'tapestries' in filename:
        dirname = 'shared/tapestries/'
    elif "variation" in filename.lower():
        dirname = "shared/variations"
    else:
        dirname = "shared/all"

    return redirect(url_for('static', filename=dirname + filename), code=301)