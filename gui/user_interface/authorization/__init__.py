from flask import Blueprint

authorization = Blueprint('authorization', __name__)

from . import views
