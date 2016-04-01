from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    hash_pass = db.Column(db.String(15), index=True, unique=False)
