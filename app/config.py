# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
import random
import string
from dotenv import load_dotenv

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    UPLOAD_FOLDER = 'app/static/uploads/'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


    load_dotenv()
    # Set up the App SECRET_KEY
    SECRET_KEY = os.getenv('SECRET_KEY', None)
    if not SECRET_KEY:
        SECRET_KEY = ''.join(random.choice(string.ascii_lowercase) for i in range(32))

    # CDN Support Settings
    CDN_DOMAIN = os.getenv('CDN_DOMAIN', None)

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600


class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig,
    'Development': DevelopmentConfig
}
