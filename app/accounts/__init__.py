from flask import Blueprint

auth = Blueprint('accounts', __name__)

from . import views
