from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))

    # relationship
    # one-to-many
    chats = db.relationship('Chat', backref='user', lazy=True)
