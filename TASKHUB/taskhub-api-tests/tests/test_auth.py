import json
from faker import Faker

fake = Faker('pt_BR') # Gera dados falsos (nomes, emails)

def test_signup_success(client, fresh_db):
    """
    Testa o cadastro de um novo usuário com sucesso.
    """
    # Prepara os dados do novo usuário
    user_data = {
        "name": fake.name(),
        "email": fake.email(),
        "password": "senha_forte_123"
    }
    
    # Faz a requisição POST para /auth/signup
    response = client.post('/auth/signup', data=json.dumps(user_data), content_type='application/json')
    
    # Verifica as respostas
    assert response.status_code == 201
    assert "Usuário criado com sucesso" in response.json['message']

def test_signup_duplicate_email(client, fresh_db):
    """
    Testa a falha ao tentar cadastrar um email que já existe.
    """
    user_data = {
        "name": fake.name(),
        "email": "email_repetido@teste.com",
        "password": "senha_forte_123"
    }
    
    # Cria o primeiro usuário
    client.post('/auth/signup', data=json.dumps(user_data), content_type='application/json')
    
    # Tenta criar o segundo usuário com o mesmo email
    response = client.post('/auth/signup', data=json.dumps(user_data), content_type='application/json')
    
    # Verifica a falha
    assert response.status_code == 400
    assert "Usuário já cadastrado" in response.json['message']

def test_login_success(client, fresh_db):
    """
    Testa o login de um usuário válido.
    """
    # Primeiro, cadastra um usuário
    user_data = {
        "email": "login@teste.com",
        "password": "senha_123"
    }
    client.post('/auth/signup', data=json.dumps(user_data), content_type='application/json')
    
    # Tenta fazer login
    response = client.post('/auth/login', data=json.dumps(user_data), content_type='application/json')
    
    # Verifica o sucesso e o token
    assert response.status_code == 200
    assert "access_token" in response.json

def test_login_invalid_credentials(client, fresh_db):
    """
    Testa o login com email ou senha incorretos.
    """
    response = client.post('/auth/login', data=json.dumps({
        "email": "naoexiste@teste.com",
        "password": "senha_errada"
    }), content_type='application/json')
    
    assert response.status_code == 401
    assert "Credenciais inválidas" in response.json['message']