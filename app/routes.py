from flask import render_template, request, redirect, send_file, url_for, flash
from app import app, db
from modules.passBuddy import *
from modules.BOFH import *
from modules.badape import *
from modules.yugioh import *
from modules.skyrim import *
import smtplib
import sqlite3
import geocoder

from hashids import Hashids

def emailSender(content):
    to = "5714779283@tmomail.net"
    sender = "steven.haering@gmail.com"
    key = "wilkbcaineyzjein"
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender, key)
    server.sendmail(sender,to,content)


'''
small_title="Title", description="Description",image_url="image.jpg", 
description
image_url
		'''

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
    return render_template('index.html',  small_title="Steve's Random Python Website",big_title="Steve's Random Python Website", description="Description",image_url="image.jpg")


# Captain website
@app.route('/captain.html')
def captain():
    return render_template('captain.html', small_title="BITCHES AND HOES", description="Captain Memorial Website",image_url="pm.png")


# Captain website
@app.route('/fuckingip.html')
def fuckingip():
    # ip_addr = request.environ['REMOTE_ADDR']
    data = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    loc_data = ip = geocoder.ip(data)


    return render_template('fuckingip.html', ip=loc_data['ip'],address=loc_data['address'],hostname=loc_data['hostname'],lat=loc_data['lat'],lon=loc_data['lon'],isp=loc_data['org'],zipcode=loc_data['postal'])


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
        return render_template('yugioh.html', small_title="YuGiOh Card Searcher", title='YuGiOh Card Searcher', description="Description",image_url="image.jpg")


# BOFH Simulator
@app.route('/bofh.html')
def bofh():
    x = random.randint(0,465)
    response=bofh_text[x].capitalize()
    lmgtfy="https://www.google.com/search?q=" + response.replace(" ","+")

    return render_template('bofh.html', small_title='IT Help Desk', response=response, link=lmgtfy, description="Description",image_url="image.jpg")


# Text Messages
@app.route('/secure/texts.html', methods=['POST'])
def texts():
    ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    if request.method == 'POST' and '216.36.27.41' in ip:
        emailSender(request.headers.get('content'))
    else:
        requests.get("https://api.telegram.org/bot5585546662:AAG4_54V68C4howzaqkVwsRTW5WAQeYAH5c/sendMessage?chat_id=-426528357&text=Unauthorized API Usage from {}".format(ip))

# Password generator
@app.route('/pass.html', methods=['GET', 'POST'])
def passbuddy():
    if request.method == 'POST':
        result = request.form
    elif request.method == 'GET':
        result="kids"
    kid_count,teen_count,adult_count,swear_count,xxx_count = getCount()
    passwords, plaintexts = getWords(result)
    password = passwords[1] + passwords[0] + getSpecial()
    password = ''.join(addCap(password))
    plaintext = plaintexts[1].capitalize()  +" "+ plaintexts[0].capitalize()
    return render_template('pass.html', small_title="Steve's Awesome Password Generator", description="Description",image_url="image.jpg", password=password, plaintext=plaintext, kid_count=kid_count, teen_count=teen_count ,adult_count=adult_count, swear_count=swear_count, xxx_count=xxx_count)


# Bad Ape
@app.route('/badape.html', methods=['GET', 'POST'])
def badape():
    meltdownScore=""
    meltPosts=""
    meltComments=""
    if request.method == 'POST':
        data = request.form.to_dict()
        meltdownScore, meltPosts, meltComments = meltdownCalc(data['Name'])

    print(meltdownScore, meltPosts, meltComments)
    return render_template('badape.html', small_title='ShillScore Calculator', description="Description",image_url="image.jpg", response=meltdownScore, meltPosts=meltPosts,meltComments=meltComments)


# Shows various things I've worked on
@app.route('/projects.html')
def projects():
    return render_template('projects.html', small_title='Projects', description="Description",image_url="image.jpg")

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

        return render_template('shorts.html', small_title="URL Shortener", short_url=short_url, description="Description",image_url="image.jpg")

    return render_template('shorts.html', small_title="URL Shortener", description="Description",image_url="image.jpg")


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
                     (clicks+1, original_id))

        conn.commit()
        conn.close()
        return redirect(original_url)
    else:
        flash('Invalid URL')
        num = random.randint(0,3)
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

