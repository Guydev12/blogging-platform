from app import db
from datetime import datetime
from flask_login import UserMixin


# The association table of Article and Tag
article_tag = db.Table('article_tag',
    db.Column('article_id', db.Integer, db.ForeignKey('article.id', ondelete='CASCADE') ,primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE'), primary_key=True)
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hash = db.Column(db.String(256), nullable= False)
    

    articles = db.relationship('Article', backref='author', lazy=True)
    profile = db.relationship('Profile', backref='user', uselist=False)

    def to_dict(self):
            return {"id": self.id, "username": self.username}

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
    # Relationship with TAg
    tags = db.relationship('Tag', secondary=article_tag, back_populates='articles')
    def __repr__(self):
        return f"<Article {self.author.username}, {self.title} {self.content} {self.created_at}>"

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable= False)

    # Relationship with Article
    articles = db.relationship('Article', secondary=article_tag, back_populates='tags')
    def __repr__(self):
        return f"<Tag {self.name}, {self.id} >"


