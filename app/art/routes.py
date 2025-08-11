from flask import Blueprint, request, render_template, redirect, url_for, send_file
import requests
from flask import render_template, request
from app import app
import random
from flask import Blueprint
from variations import *

from flask import Blueprint, request, render_template, redirect, url_for, send_file
import requests

import socket
import socket

from app.art import blueprint

art = Blueprint('art', __name__)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def secCheck(address):
    data1 = socket.gethostbyname_ex("thc-lab.net")
    data2 = socket.gethostbyname_ex("home.thc-lab.net")
    total = list(data1 + data2)
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
        return "Hey, you're not THC!"


@blueprint.route('/art.html', methods=['GET'])
def art():
    return render_template('art/art.html')


@blueprint.route('/variation', methods=['POST'])
def variation():
    AI = oldOpenAI()

    result = request.form

    data = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    if secCheck(data) and result['code'] == 'Yesbecausethisissecure101$':

        new_urls = AI.variation(result['url'])

        return "\n".join(new_urls)

    else:
        return "Hey, you're not THC!"

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