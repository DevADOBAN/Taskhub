import pytest
from app import create_app, db

# Importa os modelos para poder criá-los
from app.models import User, Task 

@pytest.fixture(scope='module')
def app():
    """
    Cria uma instância do app Flask para os testes.
    Usa um banco de dados em memória (SQLite) para ser mais rápido.
    """
    app = create_app()
    app.config.update({
        "TESTING": True,
        # Usa um banco de dados em memória para os testes
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:", 
    })

    # Cria o contexto do app e o banco de dados
    with app.app_context():
        db.create_all()
        yield app # "Entrega" o app para os testes
        db.drop_all() # Limpa tudo no final

@pytest.fixture()
def client(app):
    """
    Cria um "cliente" de teste que pode fazer requisições (GET, POST, etc.)
    """
    return app.test_client()

@pytest.fixture()
def runner(app):
    """
    Cria um "executor" de CLI, se necessário.
    """
    return app.test_cli_runner()

@pytest.fixture(scope='function')
def fresh_db(app):
    """
    Garante que o banco de dados esteja limpo para CADA teste.
    """
    with app.app_context():
        db.drop_all()
        db.create_all()

import json
from app.models import User
from app import bcrypt

@pytest.fixture(scope='function')
def authenticated_client(client, fresh_db):
    """
    Cria um usuário de teste, faz login e retorna o cliente 
    junto com o token de acesso e o ID do usuário.
    """
    # 1. Cria o usuário diretamente no DB
    password = "senha_teste_123"
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    test_user = User(email="test@user.com", name="Test User", password_hash=hashed_password)
    
    with client.application.app_context():
        db.session.add(test_user)
        db.session.commit()
        user_id = test_user.id

    # 2. Faz login para obter o token
    login_data = {"email": "test@user.com", "password": password}
    response = client.post('/auth/login', data=json.dumps(login_data), content_type='application/json')
    token = response.json['access_token']
    
    # 3. Retorna o cliente, o token e o ID do usuário para os testes
    return {
        "client": client,
        "token": token,
        "user_id": user_id
    }