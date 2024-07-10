from flask_sqlalchemy import SQLAlchemy

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
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    profile = db.relationship('Profile', backref='user', uselist=False)
