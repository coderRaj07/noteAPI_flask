from flask import Blueprint
from app.controllers.auth_controller import signup, login

auth_routes = Blueprint('auth_routes', __name__)

auth_routes.add_url_rule('/signup', 'signup', signup, methods=['POST'])
auth_routes.add_url_rule('/login', 'login', login, methods=['POST'])
