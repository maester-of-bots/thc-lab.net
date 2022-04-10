from flask import render_template, request, redirect
from app import app
from passBuddy import *
from BOFH import *
from badape import *

# Main page, there's nothing here...
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', big_title="Steve's Random Python Website", small_title='Home Page')


# Captain website
@app.route('/captain.html')
def captain():
    return render_template('captain.html', title='BITCHES AND HOES')


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


# Error Handling
@app.errorhandler(404)
def hahafuckyou_1(e):
    # note that we set the 404 status explicitly
    return redirect("http://thc-lab.net:8080", code=302)


@app.errorhandler(400)
def hahafuckyou_2(e):
    # note that we set the 404 status explicitly
    return redirect("http://thc-lab.net:8080", code=302)
