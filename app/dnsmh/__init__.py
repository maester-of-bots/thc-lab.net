from flask import Blueprint

blueprint = Blueprint(
    'dns_blueprint',
    __name__,
    url_prefix=''
)
