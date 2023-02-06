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
from modules.sql import *

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
    db = DB.get_db()
    conn = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return conn


hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])
# hashids = Hashids(min_length=4, salt='fuckiagbo')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# x


"""
#####################################################################
Home Pages
#####################################################################
"""




@app.route('/sitemap.xml')
def sitemap():
    return send_file('sitemap.xml')


# Main page, there's nothing here...
@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html',
                           small_title="Steve's Random Python Website",
                           big_title="Steve's Random Python Website",
                           description="Description",
                           image_url="image.jpg")


@app.route('/about/status.html')
def status():
    return render_template('about/status.html',
                           small_title="Status Page",
                           description="All the things I'm running")


@app.route('/about/shill.html')
def shill():
    return render_template('about/shill.html',
                           small_title="Shill Page",
                           description="For money or something")


@app.route('/about')
def about():
    return render_template('about/about.html')

@app.route('/about/recs.html')
def recs():
    return render_template('about/recs.html')


"""
#####################################################################
Link Shortener Function / Page
#####################################################################
"""
@app.route('/prd/shorts.html', methods=('GET', 'POST'))
def shorts():

    if request.method == 'POST':
        url = request.form['url']

        if not url:
            flash('The URL is required!')
            return redirect(url_for('shorts'))
        else:

            DB.post_url(url)

            url_id = DB.get_url(url)[0]
            hashid = hashids.encode(url_id)
            short_url = request.host_url + hashid
            print(hashid)

            return render_template('prd/shorts.html',
                                   small_title="URL Shortener",
                                   short_url=short_url,
                                   description="Description",
                                   image_url="image.jpg")
    else:

        return render_template('prd/shorts.html',
                               small_title="URL Shortener",
                               description="Description",
                               image_url="image.jpg")


@app.route('/<id>')
def url_redirect(id):

    temp_url = hashids.decode(id)

    if temp_url:
        temp_url2 = temp_url[0]
        original_url = DB.get_url_for_redirect(temp_url2)
        return redirect(original_url)

    else:
        flash('Invalid URL')
        num = random.randint(0, 3)
        if num == 0:
            return redirect('errors/404.html')
        elif num == 1:
            return redirect('errors/400.html')
        elif num == 2:
            return redirect('errors/666.html')
        # return redirect(url_for('index'))



"""
#####################################################################
Mostly Completed Projects
#####################################################################

"""

@app.route('/prd/fuckingip.html')
def fuckingip():
    # ip_addr = request.environ['REMOTE_ADDR']
    data = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    loc_data = geocoder.ip(data).json
    if 'hostname' in loc_data.keys():
        hostname = loc_data['hostname']
    else:
        hostname = ''
    return render_template('prd/fuckingip.html',
                           ip=loc_data['ip'],
                           address=loc_data['address'],
                           hostname=hostname,
                           lat=loc_data['lat'],
                           lon=loc_data['lng'],
                           isp=loc_data['org'],
                           isp_url="https://ipinfo.io/" + loc_data['org'].split(" ")[0],
                           zipcode=loc_data['postal'])






@app.route('/prd/bofh.html')
def bofh():
    x = random.randint(0, 465)
    response = bofh_text[x].capitalize()
    lmgtfy = "https://www.google.com/search?q=" + response.replace(" ", "+")

    return render_template('prd/bofh.html',
                           small_title='IT Help Desk',
                           response=response,
                           link=lmgtfy,
                           description="Description",
                           image_url="image.jpg")



"""
#####################################################################
Mostly Unfinished Projects
#####################################################################
"""


@app.route('/ongoing')
def ongoing():
    return render_template('/ongoing/ongoing.html',
                           small_title='Projects',
                           description="Description",
                           image_url="image.jpg")

# Password generator
@app.route('/ongoing/pass.html', methods=['GET', 'POST'])
def passbuddy():
    if request.method == 'POST':
        result = request.form
    elif request.method == 'GET':
        result = "kids"
    else:
        result = 'kids'
    kid_count, teen_count, adult_count, swear_count, xxx_count = getCount()
    passwords, plaintexts = getWords(result)
    password = passwords[1] + passwords[0] + getSpecial()
    password = ''.join(addCap(password))
    plaintext = plaintexts[1].capitalize() + " " + plaintexts[0].capitalize()
    return render_template('ongoing/pass.html',
                           small_title="Steve's Awesome Password Generator",
                           description="Description",
                           image_url="image.jpg",
                           password=password,
                           plaintext=plaintext,
                           kid_count=kid_count,
                           teen_count=teen_count,
                           adult_count=adult_count,
                           swear_count=swear_count,
                           xxx_count=xxx_count)



# Base website for Vizzy T, this probably doesn't work well
@app.route('/ongoing/vizzyt.html')
def vizzyt():
    westeros = os.listdir('app/static/img/FFS/MiddleEarth')
    middle_earth = os.listdir('app/static/img/FFS/Westeros')

    return render_template('ongoing/vizzyt.html',
                           pics=(westeros + middle_earth))


# Dreadfully under-implemented YuGiOh site
@app.route('/ongoing/yugioh.html', methods=['GET', 'POST'])
def yugioh():
    if request.method == 'POST':
        result = request.form.to_dict()['id']
        for card in cards:
            if card.id == int(result):
                data = card.getInfo()
                return render_template('ongoing/yugioh.html',
                                       small_title='YuGiOh Card Searcher',
                                       response=data)
    else:
        return render_template('ongoing/yugioh.html',
                               small_title="YuGiOh Card Searcher",
                               title='YuGiOh Card Searcher',
                               description="Description",
                               image_url="image.jpg")


"""
#####################################################################
Endpoints - Mostly just the Art shit
#####################################################################
"""


@app.route('/art.html', methods=['POST'])
def art_post():
    result = request.form

    data = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

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


@app.route('/ffs/<pic>')
def ffs_pic(pic):
    return send_file(f'static/img/FFS/Westeros/{pic}')



"""
#####################################################################
Very Old!!
#####################################################################
"""

# Funny website for the Captain
@app.route('/legacy/captain.html')
def captain():

    return render_template('legacy/captain.html',
                           small_title="BITCHES AND HOES",
                           description="Captain Memorial Website",
                           image_url="pm.png")
# Bad Ape
@app.route('/legacy/badape.html', methods=['GET', 'POST'])
def badape():
    meltdownScore = ""
    meltPosts = ""
    meltComments = ""
    if request.method == 'POST':
        data = request.form.to_dict()
        meltdownScore, meltPosts, meltComments = meltdownCalc(data['Name'])

    print(meltdownScore, meltPosts, meltComments)
    return render_template('legacy/badape.html',
                           small_title='ShillScore Calculator',
                           description="Description",
                           image_url="image.jpg",
                           response=meltdownScore,
                           meltPosts=meltPosts,
                           meltComments=meltComments)
"""
#####################################################################
ERRORS!!
#####################################################################
"""


# Error Handling
@app.errorhandler(404)
def hahafuckyou_1(e):
    # note that we set the 404 status explicitly
    return render_template('errors/404.html')
    # return redirect("http://thc-lab.net:8080", code=302)


@app.errorhandler(400)
def hahafuckyou_2(e):
    # note that we set the 404 status explicitly
    return render_template('errors/400.html')
    # return redirect("http://thc-lab.net:8080", code=302)


@app.route('/errors/404.html')
def x404():
    return render_template('errors/404.html')


@app.route('/errors/400.html')
def x400():
    return render_template('errors/400.html')


@app.route('/errors/666.html')
def x666():
    return render_template('errors/666.html')

