from flask import Blueprint
# Name of blueprint and location of the blueprint
auth = Blueprint("auth", __name__)
from . import views
