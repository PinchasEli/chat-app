import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User


app = create_app()


with app.app_context():
    for i in range(20):
        username = f'user_{i}'
        password = f'password_{i}'
        user = User(username=username, password=password)
        db.session.add(user)

    db.session.commit()

    print("Users inserted successfully.")
