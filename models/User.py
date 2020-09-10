from application import db
from werkzeug.security import generate_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    passwd = db.Column(db.String(120))
    is_valid = db.Column(db.Boolean)

    def __init__(self, username, passwd, is_valid=True):
        self.username = username
        self.passwd = generate_password_hash(passwd)
        self.is_valid = is_valid