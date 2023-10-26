

import os
from importlib import import_module

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# Initialize local DB, for...reasons, I don't think we need it.
db = SQLAlchemy()

# Initialize the LoginManager, this we need
login_manager = LoginManager()


# Function for registering extensions (DB and Login Manager)
def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def configure_database(app):
    @app.before_first_request
    def initialize_database():
        try:
            db.create_all()
        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e))

            # fallback to SQLite
            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')

            print('> Fallback to SQLite ')
            db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(config)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    login_manager = LoginManager()
    login_manager.login_view = 'auth_blueprint.login'
    login_manager.init_app(app)

    with app.app_context():
        from app.auth.models import User
        # from auth.models import User

        @login_manager.user_loader
        def load_user(user_id):
            # since the user_id is just the primary key of our user table, use it in the query for the user
            return User.query.get(int(user_id))

        app.jinja_env.globals.update(isinstance=isinstance)

        register_extensions(app)

        for module in ['art', 'auth', 'badape', 'BOFH', 'captain', 'errors','home','minecraft','password_gen','shorts','YuGiOh']:
            module = import_module(f'app.{module}.routes')
            app.register_blueprint(module.blueprint)
            print(f'Loaded {module}')

    configure_database(app)

    return app
