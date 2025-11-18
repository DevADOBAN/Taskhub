# app/models.py
from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)

    tasks = db.relationship('Task', backref='owner', lazy=True)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # Obrigatório
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), nullable=False, default='Média')
    status = db.Column(db.String(20), nullable=False, default='Pendente')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # CAMPO FALTANTE ADICIONADO
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }