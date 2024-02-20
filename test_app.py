import unittest
from flask import json
from app import app
import jwt
from app.models.note import Note
from app.models.user import User
from flask_jwt_extended import create_access_token
from bson import ObjectId

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.access_token = None
        self.note_id = None  # Variable to store the ID of the created note
        self.user1_id = str(ObjectId())  # Mock user 1 ID
        self.user2_id = str(ObjectId())  # Mock user 2 ID

    def test_signup(self):
        response = self.app.post('/signup',
                                data=json.dumps(dict(username='test', password='test')),
                                content_type='application/json')

        # Verify response status code and message
        if response.status_code == 201:
            data = json.loads(response.data)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'User created successfully')
        elif response.status_code == 400:
            data = json.loads(response.data)
            self.assertIn('error', data)
            if data['error'] == 'Username already exists':
                self.assertEqual(response.status_code, 400)
            else:
                self.assertEqual(response.status_code, 400)
        else:
            self.fail(f"Unexpected response status code: {response.status_code}")

    def test_login(self):
        response = self.app.post('/login',
                                 json={'username': 'test', 'password': 'test'},
                                 content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
        self.access_token = data['access_token']

    def test_create_note(self):
        self.test_login()  # Call test_login to obtain the access token

        response = self.app.post('/notes/create',
                                json={'title': 'test', 'content': 'test'},
                                content_type='application/json',
                                headers={'Authorization': 'Bearer ' + self.access_token})
        
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Note created successfully')

        # Fetch the newly created note from the database
        user_id = self.get_user_id_from_token(self.access_token)
        user = User.objects.get(id=user_id)
        new_note = Note.objects(owner=user).order_by('-created_at').first()
        self.assertIsNotNone(new_note)  # Ensure that a new note was created

        # Use the ID of the newly created note for subsequent tests
        self.note_id = str(new_note.id)

    def test_share_note(self):
        self.test_login()  # Call test_login to obtain the access token

        # Create a new note before attempting to share it
        self.test_create_note()

        response = self.app.post('/notes/share',
                                json={'noteId': str(self.note_id), 'userIds': [self.user1_id, self.user2_id]},
                                content_type='application/json',
                                headers={'Authorization': 'Bearer ' + self.access_token})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        print(data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Note shared successfully')


    def test_get_note(self):
        self.test_login()  # Call test_login to obtain the access token
        self.test_create_note()  # Create a note before attempting to retrieve it
        
        response = self.app.get(f'/notes/{self.note_id}',
                                headers={'Authorization': 'Bearer ' + self.access_token})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('content', data)
        self.assertIsNotNone(data['content'])

    def test_update_note(self):
        self.test_login()  # Call test_login to obtain the access token
        self.test_create_note()
        response = self.app.put(f'/notes/{self.note_id}',
                                json={'content': 'updated content'},
                                content_type='application/json',
                                headers={'Authorization': 'Bearer ' + self.access_token})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Note updated successfully')

    def test_get_version_history(self):
        self.test_login()  # Log in to obtain the access token
        self.test_create_note()  # Create a note before attempting to retrieve version history
        
        response = self.app.get(f'/notes/version-history/{self.note_id}',
                                headers={'Authorization': 'Bearer ' + self.access_token})
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)  # Check if the response data is a list
        for version_info in data:
            self.assertIsInstance(version_info, dict)  # Each element should be a dictionary
            self.assertIn('timestamp', version_info)  # Each version should have a 'timestamp' key
            self.assertIn('user', version_info)       # Each version should have a 'user' key
            self.assertIn('changes', version_info)    # Each version should have a 'changes' key
    

    # Add helper method to extract user id from token
    def get_user_id_from_token(self, token):
        decoded_token = self.decode_jwt_token(token)
        return decoded_token['sub']

    # Add helper method to decode JWT token
    def decode_jwt_token(self, token):
        return jwt.decode(token.split("Bearer ")[-1], app.config['SECRET_KEY'], algorithms=['HS256'])
    
    

if __name__ == '__main__':
    unittest.main()

