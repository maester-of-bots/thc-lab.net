import json
import os

from flask import Blueprint

from app.BOFH import blueprint

with open(os.path.join(os.path.dirname(__file__), 'excuses.json')) as f:
    bofh_text = json.load(f)

bofh = Blueprint('bofh', __name__)



@blueprint.route('/bofh.html')
def bofh():
    x = random.randint(0, 465)
    response = bofh_text[x].capitalize()
    lmgtfy = "https://www.google.com/search?q=" + response.replace(" ", "+")

    return render_template('BOFH/bofh.html',
                           small_title='IT Help Desk',
                           response=response,
                           link=lmgtfy,
                           description="Description",
                           image_url="image.jpg")