from app.models.note import Note
from app.models.user import User

async def share_note(note_id, usernames, owner_id):
    try:
        note_to_share = Note.objects.get(id=note_id, owner=owner_id)

        if not note_to_share:
            raise ValueError('Note not found')

        for username in usernames:
            user_to_share_with = User.objects.get(username=username)

            if not user_to_share_with:
                raise ValueError(f'User "{username}" not found')

            if str(user_to_share_with.id) == owner_id:
                raise ValueError('Cannot share a note with yourself')

            if user_to_share_with.id not in note_to_share.shared_with:
                note_to_share.shared_with.append(user_to_share_with.id)
                await note_to_share.save()
                user_to_share_with.notes.append(note_to_share.id)
                await user_to_share_with.save()

    except Exception as e:
        raise e
