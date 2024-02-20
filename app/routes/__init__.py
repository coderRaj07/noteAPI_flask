from flask import Blueprint

# Create Flask Blueprints for different route groups
auth_routes = Blueprint('auth_routes', __name__)
note_routes = Blueprint('note_routes', __name__)

# Import route modules to register their routes with the blueprints
from .auth_routes import *
from .note_routes import *
