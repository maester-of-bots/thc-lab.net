from flask import render_template, request, redirect, send_file, url_for, flash
from app import app, db
from modules.passBuddy import *
from modules.BOFH import *
from modules.badape import *
from modules.yugioh import *
from modules.skyrim import *
import sqlite3

from hashids import Hashids



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
    return render_template('index.html',  content_data="Steve's Random Python Website",big_title="Steve's Random Python Website", small_title='Home Page')


# Captain website
@app.route('/captain.html')
def captain():
    return render_template('captain.html', content_data="BITCHES AND HOES", title='BITCHES AND HOES')


# Bad Ape
@app.route('/yugioh.html', methods=['GET', 'POST'])
def yugioh():
    if request.method == 'POST':
        result = request.form.to_dict()['id']
        for card in cards:
            if card.id == int(result):
                data = card.getInfo()
                return render_template('yugioh.html', title='YuGiOh Card Searcher', response=data)
    else:
        return render_template('yugioh.html', content_data="YuGiOh Card Searcher", title='YuGiOh Card Searcher')


# BOFH Simulator
@app.route('/bofh.html')
def bofh():
    x = random.randint(0,465)
    response=bofh_text[x].capitalize()
    lmgtfy="https://www.google.com/search?q=" + response.replace(" ","+")

    return render_template('bofh.html', content_data="IT Help Desk", title='IT Help Desk', response=response, link=lmgtfy)


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
    return render_template('pass.html', big_title="Steve's Awesome Password Generator", small_title='Password Buddy',password=password, plaintext=plaintext, kid_count=kid_count, teen_count=teen_count ,adult_count=adult_count, swear_count=swear_count, xxx_count=xxx_count)


# Bad Ape
@app.route('/badape.html', methods=['GET', 'POST'])
def badape():
    meltdownScore=""
    meltPosts=""
    meltComments=""
    if request.method == 'POST':
        data = request.form.to_dict()
        meltdownScore, meltPosts, meltComments = meltdownCalc(data['Name'])
    return render_template('badape.html', title='ShillScore', content_data="BadApe ShillSniffer", response=meltdownScore, meltPosts=meltPosts,meltComments=meltComments)


# Shows various things I've worked on
@app.route('/projects.html')
def projects():
    return render_template('projects.html', title='Projects')

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

        return render_template('shorts.html', content_data="URL Shortener", short_url=short_url)

    return render_template('shorts.html', content_data="URL Shortener")


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
        return redirect(url_for('index'))



# Error Handling
@app.errorhandler(404)
def hahafuckyou_1(e):
    # note that we set the 404 status explicitly
    return redirect("http://thc-lab.net:8080", code=302)


@app.errorhandler(400)
def hahafuckyou_2(e):
    # note that we set the 404 status explicitly
    return redirect("http://thc-lab.net:8080", code=302)

