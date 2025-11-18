from app import create_app, db
from app.models import User, Task  # Importa os modelos para que o SQLAlchemy

# Cria a instância do aplicativo 
app = create_app()

if __name__ == '__main__':
    
    with app.app_context():
        # Cria todas as tabelas definidas em models.py
        # (Isso deve ser feito antes de iniciar o servidor)
        db.create_all()
    
    app.run(debug=True, port=5000, host='0.0.0.0')
