# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config

# Inicializa extensões (sem app ainda)
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()



def create_app(config_class=Config):
    """
    Application Factory: cria e configura o app Flask.
    Evita importações circulares importando rotas apenas aqui.
    """
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object(config_class)

    # Inicializa extensões
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors = CORS()

    # CORS: permite frontend (ex: React em localhost:3000)
    cors.init_app(
        app,
        resources={r"/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"]}},
        supports_credentials=True  # necessário para cookies/sessões
    )

    # Importa e registra rotas AQUI (evita ciclo)
    from app.routes import init_routes
    init_routes(app)

    # Cria tabelas (opcional: só em dev)
    with app.app_context():
        db.create_all()

    return app