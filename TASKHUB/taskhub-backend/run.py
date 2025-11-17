from app import create_app, db
from app.models import User, Task  # Importa os modelos para que o SQLAlchemy os "veja"

# Cria a instância do aplicativo usando a "fábrica"
app = create_app()

# Este bloco é executado quando você roda 'python run.py'
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    
    with app.app_context():
        # Cria todas as tabelas definidas em models.py
        # (Se o arquivo taskhub.db e as tabelas já existirem, não faz nada)
        db.create_all()
    
    # Inicia o servidor de desenvolvimento
    app.run(debug=True)