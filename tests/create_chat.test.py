import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Chat


app = create_app()


with app.app_context():
    for i in range(2):
        chat = Chat(user_id=2)
        db.session.add(chat)

    db.session.commit()

    print("Chats inserted successfully.")
