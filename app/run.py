# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from sys import exit

from flask_migrate import Migrate
from flask_minify import Minify

from app import create_app
from app.config import config_dict

# WARNING: Don't run with debug turned on in production!
DEBUG = 'False' # (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'


try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]
    app = create_app(app_config)
    Migrate(app)

    if not DEBUG:
        Minify(app=app, html=True, js=False, cssless=False)

    if DEBUG:
        app.logger.info('DEBUG            = ' + str(DEBUG))
        app.logger.info('Page Compression = ' + 'FALSE' if DEBUG else 'TRUE')


except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')


if __name__ == "__main__":
    app.run()

