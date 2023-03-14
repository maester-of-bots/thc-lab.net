from flask import Blueprint
from flask import render_template, redirect

import random

from app.errors import blueprint


errors = Blueprint('errors', __name__)


# Error Handling
@blueprint.errorhandler(404)
def hahafuckyou_1(e):
    # note that we set the 404 status explicitly
    return render_template('errors/404.html')
    # return redirect("http://thc-lab.net:8080", code=302)


@blueprint.errorhandler(400)
def hahafuckyou_2(e):
    # note that we set the 404 status explicitly
    return render_template('errors/400.html')
    # return redirect("http://thc-lab.net:8080", code=302)


@blueprint.route('/errors/404.html')
def x404():
    return render_template('errors/404.html')


@blueprint.route('/errors/400.html')
def x400():
    return render_template('errors/400.html')


@blueprint.route('/errors/666.html')
def x666():
    return render_template('errors/666.html')

