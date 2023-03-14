from flask import Blueprint, render_template, redirect, request

from app.password_gen import blueprint

import random
from app.password_gen.words_list import *

###############################
# Password Buddy
###############################

lastnum = [-1,-1]

def complicate_word(characters,word):
    c = list(zip(characters[0], characters[1]))
    random.shuffle(c)
    characters[0], characters[1] = zip(*c)

    for i in range(0,len(characters[0])):
        if characters[0][i] in word:
            Word = word.replace(characters[0][i],characters[1][i],1)
    try:
        return Word
    except:
        return (word+"#")

def getSpecial():
    chars=["!","@","#"]
    return chars[random.randint(0,2)]

def getNumber():
    return random.randint(0,9)

def addCap(password):
    new=list(password)
    for i in range(0, len(new)):
        if new[i].isalpha():
            new[i] = new[i].capitalize()
            return new


def getCount():
    kid_count = len(wordlist[4][0]) * len(wordlist[4][1])
    teen_count = len(wordlist[1][0]) * len(wordlist[1][1])
    adult_count = len(wordlist[0][0]) * len(wordlist[0][1])
    swear_count = len(wordlist[2][0]) * len(wordlist[2][1])
    xxx_count = len(wordlist[3][0]) * len(wordlist[3][1])
    print(kid_count, teen_count, adult_count, swear_count, xxx_count)
    return kid_count, teen_count, adult_count, swear_count, xxx_count


def getWords(result):
    if "adults" in result:
        words = wordlist[0]
        chars = adults
    if "teens" in result:
        words = wordlist[1]
        chars = teenagers
    if "swears" in result:
        words = wordlist[2]
        chars = adults
    if "sex" in result:
        words = wordlist[3]
        chars = adults
    if "kids" in result:
        words = wordlist[4]
        chars = children

    newwords = []
    plaintexts = []
    global lastnum
    for i in range(0,2):
        num1 = random.randint(0, len(words[i]))-1
        if num1==lastnum[i]:
            num1 = random.randint(0, len(words[i]))-1
        if num1==lastnum[i]:
            num1 = random.randint(0, len(words[i]))-1
        lastnum[i]=num1
        word = words[i][num1]
        plaintexts.append(word)
        newwords.append(complicate_word(chars,word))
    return newwords,plaintexts




password_gen = Blueprint('password_gen', __name__)


# Password generator
@blueprint.route('/pass.html', methods=['GET', 'POST'])
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
    return render_template('password_gen/pass.html',
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