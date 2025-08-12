from flask import Blueprint

blueprint = Blueprint(
    'git_blueprint',
    __name__,
    url_prefix=''
)
