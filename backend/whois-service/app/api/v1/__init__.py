from flask import Blueprint

bp = Blueprint('api', __name__)

from . import whois_routes
