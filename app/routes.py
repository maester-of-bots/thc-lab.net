from flask import render_template, request, redirect, send_file, url_for, flash
from app import app, db
from modules.passBuddy import *
from modules.BOFH import *
from modules.badape import *
from modules.yugioh import *
# from modules.skyrim import *
import smtplib
import sqlite3
import geocoder
import os

from hashids import Hashids
from werkzeug.utils import secure_filename


import socket

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




# Init Yugioh cards
cards = getAllCards()


def get_db_connection():
    conn = sqlite3.connect('data/database.db')
    conn.row_factory = sqlite3.Row
    return conn


hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])


# Main page, there's nothing here...
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', small_title="Steve's Random Python Website",
                           big_title="Steve's Random Python Website", description="Description", image_url="image.jpg")


# Captain website
@app.route('/captain.html')
def captain():
    return render_template('captain.html', small_title="BITCHES AND HOES", description="Captain Memorial Website",
                           image_url="pm.png")


# Captain website
@app.route('/status.html')
def status():
    return render_template('status.html', small_title="Status Page", description="All the things I'm running")


# Captain website
@app.route('/vizzyt.html')
def vizzyt():
    westeros = os.listdir('app/static/img/FFS/MiddleEarth')
    middle_earth = os.listdir('app/static/img/FFS/Westeros')
    return render_template('vizzyt.html', pics=(westeros + middle_earth))


# Captain website
@app.route('/fuckingip.html')
def fuckingip():
    # ip_addr = request.environ['REMOTE_ADDR']
    data = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    loc_data = geocoder.ip(data).json
    if 'hostname' in loc_data.keys():
        hostname = loc_data['hostname']
    else:
        hostname = ''
    return render_template('fuckingip.html', ip=loc_data['ip'], address=loc_data['address'], hostname=hostname,
                           lat=loc_data['lat'], lon=loc_data['lng'], isp=loc_data['org'],
                           isp_url="https://ipinfo.io/" + loc_data['org'].split(" ")[0], zipcode=loc_data['postal'])


# Bad Ape
@app.route('/yugioh.html', methods=['GET', 'POST'])
def yugioh():
    if request.method == 'POST':
        result = request.form.to_dict()['id']
        for card in cards:
            if card.id == int(result):
                data = card.getInfo()
                return render_template('yugioh.html', small_title='YuGiOh Card Searcher', response=data)
    else:
        return render_template('yugioh.html', small_title="YuGiOh Card Searcher", title='YuGiOh Card Searcher',
                               description="Description", image_url="image.jpg")


# BOFH Simulator
@app.route('/bofh.html')
def bofh():
    x = random.randint(0, 465)
    response = bofh_text[x].capitalize()
    lmgtfy = "https://www.google.com/search?q=" + response.replace(" ", "+")

    return render_template('bofh.html', small_title='IT Help Desk', response=response, link=lmgtfy,
                           description="Description", image_url="image.jpg")

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# x

@app.route('/art.html', methods=['POST'])
def art_post():
    result = request.form

    data = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

    print(data)

    if secCheck(data) and result['code'] == 'fuck you you fucking fuck':

        url = result['url']

        subdir = result['subdir']

        name = result['filename']

        if subdir == 'None':
            path = f'app/static/uploads/{name}'
            newpath = f'https://thc-lab.net/static/uploads/{name}'
        else:
            path = f'app/static/{subdir}/{name}'
            newpath = f'https://thc-lab.net/static/{subdir}/{name}'

        data = requests.get(url)

        with open(path,'wb') as image:
            image.write(data.content)



        return newpath

    else:
        return "Hey, you're not THC!"



@app.route('/art.html', methods=['GET'])
def art():
    return render_template('art.html')

@app.route('/display/<filename>')
def display_image(filename):
    if 'tapestries' in filename:
        return redirect(url_for('static', filename='tapestries/' + filename), code=301)
    else:
        return redirect(url_for('static', filename='uploads/' + filename), code=301)




# Password generator
@app.route('/pass.html', methods=['GET', 'POST'])
def passbuddy():
    if request.method == 'POST':
        result = request.form
    elif request.method == 'GET':
        result = "kids"
    kid_count, teen_count, adult_count, swear_count, xxx_count = getCount()
    passwords, plaintexts = getWords(result)
    password = passwords[1] + passwords[0] + getSpecial()
    password = ''.join(addCap(password))
    plaintext = plaintexts[1].capitalize() + " " + plaintexts[0].capitalize()
    return render_template('pass.html', small_title="Steve's Awesome Password Generator", description="Description",
                           image_url="image.jpg", password=password, plaintext=plaintext, kid_count=kid_count,
                           teen_count=teen_count, adult_count=adult_count, swear_count=swear_count, xxx_count=xxx_count)


# Bad Ape
@app.route('/badape.html', methods=['GET', 'POST'])
def badape():
    meltdownScore = ""
    meltPosts = ""
    meltComments = ""
    if request.method == 'POST':
        data = request.form.to_dict()
        meltdownScore, meltPosts, meltComments = meltdownCalc(data['Name'])

    print(meltdownScore, meltPosts, meltComments)
    return render_template('badape.html', small_title='ShillScore Calculator', description="Description",
                           image_url="image.jpg", response=meltdownScore, meltPosts=meltPosts,
                           meltComments=meltComments)


# Shows various things I've worked on
@app.route('/projects.html')
def projects():
    return render_template('projects.html', small_title='Projects', description="Description", image_url="image.jpg")


@app.route('/sitemap.xml')
def sitemap():
    return send_file('sitemap.xml')


@app.route('/shorts', methods=('GET', 'POST'))
def shorts():
    conn = get_db_connection()

    if request.method == 'POST':
        url = request.form['url']

        if not url:
            flash('The URL is required!')
            return redirect(url_for('shorts'))

        url_data = conn.execute('INSERT INTO urls (original_url) VALUES (?)',
                                (url,))
        conn.commit()
        conn.close()

        url_id = url_data.lastrowid
        hashid = hashids.encode(url_id)
        short_url = request.host_url + hashid

        return render_template('shorts.html', small_title="URL Shortener", short_url=short_url,
                               description="Description", image_url="image.jpg")

    return render_template('shorts.html', small_title="URL Shortener", description="Description", image_url="image.jpg")


@app.route('/404.html')
def x404():
    return render_template('404.html')


@app.route('/400.html')
def x400():
    return render_template('400.html')


@app.route('/666.html')
def x666():
    return render_template('666.html')


@app.route('/recs.html')
def recs():
    return render_template('recs.html')



@app.route('/ffs/<pic>')
def ffs_pic(pic):
    return send_file(f'static/img/FFS/Westeros/{pic}')


@app.route('/<id>')
def url_redirect(id):
    conn = get_db_connection()

    original_id = hashids.decode(id)
    if original_id:
        original_id = original_id[0]
        url_data = conn.execute('SELECT original_url, clicks FROM urls'
                                ' WHERE id = (?)', (original_id,)
                                ).fetchone()
        original_url = url_data['original_url']
        clicks = url_data['clicks']

        conn.execute('UPDATE urls SET clicks = ? WHERE id = ?',
                     (clicks + 1, original_id))

        conn.commit()
        conn.close()
        return redirect(original_url)
    else:
        flash('Invalid URL')
        num = random.randint(0, 3)
        if num == 0:
            return redirect('/404.html')
        elif num == 1:
            return redirect('/400.html')
        elif num == 2:
            return redirect('/666.html')
        # return redirect(url_for('index'))


# Error Handling
@app.errorhandler(404)
def hahafuckyou_1(e):
    # note that we set the 404 status explicitly
    return render_template('404.html')
    # return redirect("http://thc-lab.net:8080", code=302)


@app.errorhandler(400)
def hahafuckyou_2(e):
    # note that we set the 404 status explicitly
    return redirect("http://thc-lab.net:8080", code=302)
