from flask import Blueprint
from flask import render_template, redirect


from app.captain import blueprint

captain = Blueprint('captain', __name__)


"""
#####################################################################
Very Old!!
#####################################################################
"""

# Funny website for the Captain
@blueprint.route('/captain.html')
def captain():

    return render_template('captain/captain.html',
                           small_title="BITCHES AND HOES",
                           description="Captain Memorial Website",
                           image_url="pm.png")