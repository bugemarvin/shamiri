from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    '''
    User model class

    Attributes:
      id (int): User ID
      username (str): User name
      email (str): User email
      password (str): User password
    '''

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile = db.relationship('Profile', backref='user', uselist=False)


class Profile(db.Model):
    '''
    Profile model class

    Attributes:
      id (int): Profile ID
      user_id (int): User ID
      email (str): User email
      gender (str): User gender
      phone_number (str): User phone_number
      city (str): User city
      country (str): User country
      bio (str): User bio
    '''
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)
    email = db.Column(db.Text, nullable=True)
    gender = db.Column(db.Text, nullable=True)
    phone_number = db.Column(db.Text, nullable=True)
    city = db.Column(db.Text, nullable=True)
    country = db.Column(db.Text, nullable=True)
    bio = db.Column(db.Text, nullable=True)


class JournalEntry(db.Model):
    '''
    Journal Entry model class

    Attributes:
      id (int): Entry ID
      user_id (int): User ID
      title (str): Entry title
      content (str): Entry content
      category (str): Entry category
      created_at (datetime): Entry created date
    '''
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.today)

    user = db.relationship('User', backref='entries')
