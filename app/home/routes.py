from flask import Blueprint
from flask import render_template, redirect
from flask_login import (
    login_required,
    current_user
)

from flask import render_template, request, redirect, send_file, url_for, flash

# from modules.skyrim import *
import smtplib
import sqlite3
import geocoder
import os

from werkzeug.utils import secure_filename
from modules.sql import *


from app.home import blueprint

home = Blueprint('home', __name__)






@blueprint.route('/sitemap.xml')
def sitemap():
    return send_file('sitemap.xml')


# Main page, there's nothing here...
@blueprint.route('/', methods=['GET', 'POST'])
def index():

    return render_template('home/index.html',
                           small_title="Steve's Random Python Website",
                           big_title="Steve's Random Python Website",
                           description="Description",
                           image_url="image.jpg")

# Main page, there's nothing here...
@blueprint.route('/legal', methods=['GET'])
def index():

    return render_template('home/legal.html')


@blueprint.route('/status.html')
def status():
    return render_template('home/status.html',
                           small_title="Status Page",
                           description="All the things I'm running")


@blueprint.route('/shill.html')
def shill():
    return render_template('home/shill.html',
                           small_title="Shill Page",
                           description="For money or something")


@blueprint.route('/about.html')
def about():
    return render_template('home/about.html')


@blueprint.route('/recs.html')
def recs():
    return render_template('home/recs.html')


@blueprint.route('/projects.html')
def ongoing():
    return render_template('home/ongoing.html',
                           small_title='Projects',
                           description="Description",
                           image_url="image.jpg")

