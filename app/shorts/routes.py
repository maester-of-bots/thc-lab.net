from flask import Blueprint, request, render_template, redirect, flash, url_for
from hashids import Hashids
import random
from modules.sql import *

from dotenv import load_dotenv
from app.shorts import blueprint


shorts = Blueprint('shorts', __name__)
load_dotenv()
hashids = Hashids(min_length=4, salt=os.getenv('SECRET_KEY', None))


@blueprint.route('/shorts.html', methods=('GET', 'POST'))
def shorts():

    if request.method == 'POST':
        url = request.form['url']

        if not url:
            flash('The URL is required!')
            return redirect(url_for('shorts'))
        else:
            if "http" not in url.lower():
                url = "http://" + url

            DB.post_url(url, 'beta.thc-lab.net')

            url_id = DB.get_url(url, 'beta.thc-lab.net')[0]
            print(url_id)
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
        temp_url2 = temp_url[0]
        original_url = DB.get_url_for_redirect(temp_url2, 'beta.thc-lab.net')
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
