from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from configs.config import Config
from routes.auth import auth_bp
from routes.journal import entries_bp
from routes.summaries import summaries_bp
from models.model import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(entries_bp, url_prefix='/entries')
    app.register_blueprint(summaries_bp, url_prefix='/summaries')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)