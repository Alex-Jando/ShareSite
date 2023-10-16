from flask_login import UserMixin
from . import db
import secrets

class User(UserMixin, db.Model):
    id = db.Column(db.String(), primary_key=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    files = db.relationship('File')
    links = db.relationship('Link')

    def __init__(self, email, password) -> None:
        while User.query.filter_by(id=(id:=secrets.token_urlsafe(8))).first():
            pass
        self.id = id
        self.email = email
        self.password = password

class File(db.Model):
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    data = db.Column(db.LargeBinary())
    size = db.Column(db.Integer())
    public = db.Column(db.Boolean())
    user_id = db.Column(db.String(), db.ForeignKey('user.id'))

    def __init__(self, name, data, public, user_id) -> None:
        while File.query.filter_by(id=(id:=secrets.token_urlsafe(8))).first():
            pass
        self.id = id
        self.name = name
        self.data = data
        self.size = len(data)
        self.public = public
        self.user_id = user_id

class Link(db.Model):
    id = db.Column(db.String(), primary_key=True)
    url = db.Column(db.String())
    public = db.Column(db.Boolean())
    user_id = db.Column(db.String(), db.ForeignKey('user.id'))

    def __init__(self, url, public, user_id) -> None:
        while Link.query.filter_by(id=(id:=secrets.token_urlsafe(8))).first():
            pass
        self.id = id
        self.url = url
        self.public = public
        self.user_id = user_id