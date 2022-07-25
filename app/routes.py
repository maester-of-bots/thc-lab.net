from flask import render_template, request, redirect, send_file, url_for, flash
from app import app, db
from passBuddy import *
from BOFH import *
from badape import *
from yugioh import *

from datetime import datetime
from app.models import ShortUrls
from random import choice
import string


# Init Yugioh cards
cards = getAllCards()


def generate_short_id(num_of_chars: int):
    """Function to generate short_id of specified number of characters"""
    return ''.join(choice(string.ascii_letters+string.digits) for _ in range(num_of_chars))



# Main page, there's nothing here...
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', big_title="Steve's Random Python Website", small_title='Home Page')


# Captain website
@app.route('/captain.html')
def captain():
    return render_template('captain.html', title='BITCHES AND HOES')


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
        return render_template('yugioh.html', title='YuGiOh Card Searcher')


# BOFH Simulator
@app.route('/bofh.html')
def bofh():
    x = random.randint(0,465)
    response=bofh_text[x].capitalize()
    lmgtfy="https://www.google.com/search?q=" + response.replace(" ","+")

    return render_template('bofh.html', title='IT Help Desk', response=response, link=lmgtfy)


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
    return render_template('badape.html', title='ShillScore', response=meltdownScore, meltPosts=meltPosts,meltComments=meltComments)


# Shows various things I've worked on
@app.route('/projects.html')
def projects():
    return render_template('projects.html', title='Projects')

@app.route('/sitemap.xml')
def sitemap():
    return send_file('sitemap.xml')

@app.route('/shorty', methods=['GET', 'POST'])
def reroute():
    if request.method == 'POST':
        url = request.form['url']
        short_id = request.form['custom_id']

        if short_id and ShortUrls.query.filter_by(short_id=short_id).first() is not None:
            flash('Please enter different custom id!')
            return redirect(url_for('index_short'))

        if not url:
            flash('The URL is required!')
            return redirect(url_for('index_short'))

        if not short_id:
            short_id = generate_short_id(8)

        new_link = ShortUrls(
            original_url=url, short_id=short_id, created_at=datetime.now())
        db.session.add(new_link)
        db.session.commit()
        short_url = request.host_url + short_id

        return render_template('index_short.html', short_url=short_url)

    return render_template('index_short.html')

@app.route('/<short_id>')
def redirect_url(short_id):
    link = ShortUrls.query.filter_by(short_id=short_id).first()
    if link:
        return redirect(link.original_url)
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

