from flask import Blueprint, request, render_template, redirect, url_for, send_file
import requests

import socket

from app.art import blueprint

art = Blueprint('art', __name__)





'''
def get_db_connection():
    db = DB.get_db()
    conn = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return conn
'''


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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



@blueprint.route('/art.html', methods=['POST'])
def art_post():
    result = request.form

    data = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    if secCheck(data) and result['code'] == 'fuck you you fucking fuck':

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