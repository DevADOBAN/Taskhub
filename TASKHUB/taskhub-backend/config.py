import os

# Pega o caminho absoluto do diretório onde este arquivo está
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configurações do aplicativo."""
    
    # Chave secreta para o JWT. Mude isso para algo aleatório!
    JWT_SECRET_KEY = 'minha-chave'
    
    # Configuração do banco de dados SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'taskhub.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False