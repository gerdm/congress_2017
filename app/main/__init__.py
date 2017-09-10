from flask import Blueprint
#the blueprint name and the module or package where the blueprint is located.
main = Blueprint("main", __name__)
from . import views, errors
