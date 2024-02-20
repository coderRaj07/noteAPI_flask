**Readme File**

**Testing Endpoints:**

Below are the instructions to test the endpoints of your Flask application. These commands should be run inside the virtual environment (`venv`) to ensure proper isolation and dependency management.

**1. POST /notes/share**

**Description:** Share a note with multiple users.

**Request Payload:**
- **noteId**: String, required. The ID of the note to be shared.
- **userIds**: List of strings, required. The IDs of the users with whom the note will be shared.

**Example Request:**
```
POST localhost:5000/notes/share
{
  "noteId":"65d38c1fee456d6aeb5f5ac2",
  "userIds":["65d3e9f16b933afc28af6651"]
}
```

**2. GET /notes/version-history/{noteId}**

**Description:** Get the version history of a note.

**URL Parameter:**
- **noteId**: String, required. The ID of the note to retrieve the version history for.

**Example Request:**
```
GET localhost:5000/notes/version-history/65d38c1fee456d6aeb5f5ac2
```

**3. POST /notes/share**

**Description:** Share a note.

**Request Payload:** _(Payload details not provided)_

**Example Request:**
```
POST localhost:5000/notes/share
```

**4. PUT /notes/{noteId}**

**Description:** Update the content of a note.

**URL Parameter:**
- **noteId**: String, required. The ID of the note to be updated.

**Request Payload:**
- **content**: String, required. The new content of the note.

**Example Request:**
```
PUT localhost:5000/notes/65d38c1fee456d6aeb5f5ac2
{
  "content":"neofi_3"
}
```

**5. GET /notes/{noteId}**

**Description:** Get the details of a note.

**URL Parameter:**
- **noteId**: String, required. The ID of the note to retrieve details for.

**Example Request:**
```
GET localhost:5000/notes/65d38c1fee456d6aeb5f5ac2
```

**6. POST /notes/create**

**Description:** Create a new note.

**Request Payload:**
- **title**: String, required. The title of the new note.
- **content**: String, required. The content of the new note.

**Example Request:**
```
POST localhost:5000/notes/create
{
  "title":"neofi_2",
  "content":"neofi_2"
}
```

**Authentication:**

All endpoints require Bearer token authentication. To obtain an access token, follow these steps:

1. **POST /login**: Generate an access token by providing valid credentials.

**Request Payload:**
- **username**: String, required. The username of the user.
- **password**: String, required. The password of the user.

**Example Request:**
```
POST http://localhost:5000/login
{
  "username":"username",
  "password": "password"
}
```

2. **POST /signup**: Sign up to create a new account.

**Request Payload:**
- **username**: String, required. The username for the new account.
- **password**: String, required. The password for the new account.

**Example Request:**
```
POST http://localhost:5000/signup
{
  "username":"username1",
  "password": "password1"
}
```

**Running the APIs:**

To run the APIs, follow these instructions:

1. Ensure you have Python installed on your system.

2. Set up and activate the virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies by running:
   ```
   pip install -r requirements.txt
   ```

4. Start the Flask application by executing:
   ```
   python3 run.py
   ```

5. Once the server is running, you can test the endpoints using tools like Postman or by sending HTTP requests programmatically.

**Note:** Replace `localhost:5000` with the appropriate host and port if your Flask application is running on a different address.

**Make sure to secure your endpoints and handle sensitive data appropriately, especially when dealing with authentication and user data.**
