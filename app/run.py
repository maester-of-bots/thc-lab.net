# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from sys import exit

from flask_migrate import Migrate
from flask_minify import Minify

from app import create_app, db
from app.config import config_dict

# WARNING: Don't run with debug turned on in production!
DEBUG = 'False' # (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'


def configure_database(app):
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

    # Call initialize_database immediately instead of using before_first_request
    with app.app_context():
        initialize_database()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]
    app = create_app(app_config)
    # configure_database(app)
    Migrate(app, db)

    if not DEBUG:
        Minify(app=app, html=True, js=False, cssless=False)

    if DEBUG:
        app.logger.info('DEBUG            = ' + str(DEBUG))
        app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE')
        app.logger.info('DBMS             = ' + app_config.SQLALCHEMY_DATABASE_URI)


except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')


if __name__ == "__main__":
    app.run()

