from flask import Blueprint
from app.controllers.note_controller import create_note, get_note, share_note_route, update_note, get_version_history

note_routes = Blueprint('note_routes', __name__)

note_routes.add_url_rule('/notes/create', 'create_note', create_note, methods=['POST'])
note_routes.add_url_rule('/notes/<id>', 'get_note', get_note, methods=['GET'])
note_routes.add_url_rule('/notes/share', 'share_note', share_note_route, methods=['POST'])
note_routes.add_url_rule('/notes/<id>', 'update_note', update_note, methods=['PUT'])
note_routes.add_url_rule('/notes/version-history/<id>', 'get_version_history', get_version_history, methods=['GET'])
