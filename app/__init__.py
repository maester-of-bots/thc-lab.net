from importlib import import_module

from flask import Flask

def create_app(config):
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(config)

    modules = ['art', 'home', 'shorts', 'password_gen', 'BOFH', 'dnsmh', 'badape', 'github',
               'subnet_calculator', 'emailsmh']

    with app.app_context():

        for directory in modules:

            module = import_module(f'app.{directory}.routes')
            app.register_blueprint(module.blueprint)

        print(f'Modules loaded.')

    return app
