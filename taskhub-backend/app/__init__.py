# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # CORS CORRIGIDO — permite o front rodando em 127.0.0.1:8000
    CORS(
        app,
        resources={r"/*": {"origins": ["http://127.0.0.1:8000", "http://localhost:8000"]}},
        supports_credentials=True
    )

    from app.routes import init_routes
    init_routes(app)

    with app.app_context():
        db.create_all()

    return app
