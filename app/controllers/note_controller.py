import json
from bson import ObjectId
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app.models.user import User
from app.models.note import Note
from app.models.note_version import NoteVersion
from app.services.note_service import share_note 

@jwt_required()
def create_note():
    try:
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        data = request.get_json()
        note = Note(title=data['title'], content=data['content'], owner=user)
        note.save()

        note_dict = {
            'id': str(note.id),
            'title': note.title,
            'content': note.content,
            'owner': str(note.owner.id)
        }
        
        return jsonify({'message': 'Note created successfully', 'note': note_dict}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@jwt_required()
def get_note(id):
    try:
        note_json = Note.objects.get(id=id).to_json()
        note = json.loads(note_json)
        user_id = get_jwt_identity()
        print("User ID:", user_id)
        print("Note Owner:", note)
        
        # Ensure that the user has access to the note
        if note['owner']['$oid'] != user_id and user_id not in [str(user['$oid']) for user in note['shared_with']]:
            return jsonify({'error': 'Unauthorized access to the note'}), 403
        
        return jsonify({'content': note['content']}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@jwt_required()
def share_note_route():
    try:
        data = request.get_json()
        note_id = data.get('noteId')
        user_ids = data.get('userIds', [])

        if not isinstance(user_ids, list):
            raise ValueError("'userIds' field must be a list")

        if not user_ids:
            raise ValueError("No user IDs provided for sharing")

        # Get the note from the database
        note = Note.objects.get(id=note_id)
        
        # Check if the note exists
        if not note:
            return jsonify({'error': 'Note not found'}), 404

        # Check if the user has permission to share the note
        user_id = get_jwt_identity()
        if str(note.owner.id) != user_id:
            return jsonify({'error': 'You do not have permission to share this note'}), 403

        # Fetch previous shared_with list
        prev_shared_with = [str(user.id) for user in note.shared_with]

        # Convert user IDs to ObjectId
        user_ids = [str(ObjectId(user_id)) for user_id in user_ids]

        # Push our ID to the shared_with list and remove duplicates
        shared_with_ids = list(set(prev_shared_with + user_ids))
        
        # Update shared_with field
        note.shared_with = [ObjectId(user_id) for user_id in shared_with_ids]
            
        # Save the note
        note.save()

        return jsonify({'message': 'Note shared successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400







@jwt_required()
def update_note(id):
    try:
        note_json = Note.objects.get(id=id).to_json()
        data = json.loads(note_json)
        new_content = data.get('content', '')
        if not new_content.strip():
            raise ValueError('Content cannot be empty')

        user_id = get_jwt_identity()
        if data['owner']['$oid'] != user_id and user_id not in [str(user['$oid']) for user in data['shared_with']]:
            return jsonify({'error': 'Unauthorized access to update the note'}), 403

        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        updated_content = f"{data['content']}\n\n{timestamp}: {new_content}"
        
        # Update the note content and timestamp
        Note.objects(id=id).update(content=updated_content, updated_at=datetime.utcnow())

        # Update NoteVersion
        note_version = NoteVersion(note=Note.objects.get(id=id), user=User.objects.get(id=user_id), changes=new_content)
        note_version.save()

        return jsonify({'message': 'Note updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@jwt_required()
def get_version_history(id):
    try:
        note = Note.objects.get(id=id)
        user_id = get_jwt_identity()
        if str(note.owner.id) != user_id and user_id not in [str(user.id) for user in note.shared_with]:
            return jsonify({'error': 'Unauthorized access to the version history of the note'}), 403

        version_history = NoteVersion.objects(note=note).order_by('created_at')
        response_data = []
        for version in version_history:
            version_info = {
                'timestamp': version.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'user': version.user.username,
                'changes': version.changes
            }
            response_data.append(version_info)

        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
