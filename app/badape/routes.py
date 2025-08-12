from flask import Blueprint
from flask import render_template, request

from app.badape import blueprint
from dotenv import load_dotenv
import os
import requests
import json
badape = Blueprint('badape', __name__)

@blueprint.route('/badape.html', methods=('GET', 'POST'))
def dns():
    if request.method == 'POST':
        domain = request.form['domain']
        return render_template('badape/badape.html', data="Dunno man, something broke.")

    else:
        return render_template('badape/badape.html')