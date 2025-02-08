from app import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hash = db.Column(db.String(256), nullable= False)
    

    articles = db.relationship('Article', backref='author', lazy=True)
    profile = db.relationship('Profile', backref='user', uselist=False)

    def __repr__(self):
        return f"<User {self.username} {self.email}>"

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # FIXED

    def __repr__(self):
        return f'<Profile {self.user_id} {self.bio}>'

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # FIXED
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # FIXED

    def __repr__(self):
        return f"<Article {self.author.username}, {self.title} {self.content} {self.created_at}>"