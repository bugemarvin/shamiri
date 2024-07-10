from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config.from_envvar('FLASK_APP')
app.config.from_envvar('FLASK_ENV')
app.config.from_envvar('SECRET_KEY')
app.config.from_envvar('DATABASE_URL')
app.config.from_envvar('SQLALCHEMY_TRACK_MODIFICATIONS')
app.config.from_envvar('JWT_SECRET_KEY')