from flask import Blueprint, request, render_template, redirect, flash, url_for
from hashids import Hashids
import os
import random
from modules.sql import *

from dotenv import load_dotenv
from app.shorts import blueprint

load_dotenv()
hashids = Hashids(min_length=4, salt=os.getenv('SECRET_KEY', None))

DOMAIN = 'thc-lab.net'

ERROR_PAGES = ['errors/404.html', 'errors/400.html', 'errors/666.html']


@blueprint.route('/shorts.html', methods=('GET', 'POST'))
def shorts():
    if request.method == 'POST':
        url = request.form.get('url', '').strip()

        if not url:
            flash('The URL is required!')
            return redirect(url_for('shorts_blueprint.shorts'))

        if "http" not in url.lower():
            url = "http://" + url

        DB.post_url(url, DOMAIN)
        url_id = DB.get_url(url, DOMAIN)[0]
        hashid = hashids.encode(url_id)
        short_url = request.host_url + hashid

        return render_template('shorts/shorts.html',
                               small_title="URL Shortener",
                               short_url=short_url,
                               description="Description",
                               image_url="image.jpg")
    else:
        return render_template('shorts/shorts.html',
                               small_title="URL Shortener",
                               description="Description",
                               image_url="image.jpg")


@blueprint.route('/<id>')
def url_redirect(id):
    temp_url = hashids.decode(id)

    if temp_url:
        original_url = DB.get_url_for_redirect(temp_url[0], DOMAIN)
        return redirect(original_url)
    else:
        flash('Invalid URL')
        return render_template(random.choice(ERROR_PAGES))
