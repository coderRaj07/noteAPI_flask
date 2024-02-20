from flask import Flask
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = MongoEngine(app)
jwt = JWTManager(app)

from app.routes.auth_routes import auth_routes
from app.routes.note_routes import note_routes

app.register_blueprint(auth_routes)
app.register_blueprint(note_routes)
