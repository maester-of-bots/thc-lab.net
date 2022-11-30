from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from decouple import config





app = Flask(__name__, static_url_path='/static')

app.config.from_object(config("APP_SETTINGS"))
app.config['SECRET_KEY'] = 'ughokaywhatthefuckbroWHYYY1111@#!'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
UPLOAD_FOLDER = 'app/static/uploads/'

app.secret_key = "ughokaywhatthefuckbroWHYYY1111"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024





from app import routes
