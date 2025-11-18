# app/routes.py
from flask import request, jsonify
from app import db, bcrypt
from app.models import User, Task
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.exc import SQLAlchemyError
import traceback


def init_routes(app):

    # ======================================================
    # SIGNUP
    # ======================================================
    @app.route("/auth/signup", methods=["POST"])
    def signup():
        if not request.is_json:
            return jsonify({"message": "JSON requerido"}), 400

        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return jsonify({"message": "Todos os campos são obrigatórios"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"message": "Email já cadastrado"}), 400

        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(
            name=name,
            email=email,
            password_hash=hashed_pw
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "Usuário criado com sucesso"}), 201

    # ======================================================
    # LOGIN
    # ======================================================
    @app.route("/auth/login", methods=["POST"])
    def login():
        if not request.is_json:
            return jsonify({"message": "JSON requerido"}), 400

        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"message": "Email e senha são obrigatórios"}), 400

        user = User.query.filter_by(email=email).first()

        if not user or not bcrypt.check_password_hash(user.password_hash, password):
            return jsonify({"message": "Credenciais inválidas"}), 401

        # TOKEN CORRETO – identity deve ser string
        token = create_access_token(identity=str(user.id))

        return jsonify({"access_token": token}), 200

    # ======================================================
    # USER INFO
    # ======================================================
    @app.route("/auth/me", methods=["GET"])
    @jwt_required()
    def get_me():
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user:
            return jsonify({"message": "Usuário não encontrado"}), 404

        return jsonify({
            "id": user.id,
            "email": user.email,
            "name": user.name
        }), 200

    # ======================================================
    # CREATE TASK
    # ======================================================
    @app.route("/api/tasks", methods=["POST"])
    @jwt_required()
    def create_task():
        try:
            user_id = int(get_jwt_identity())

            if not request.is_json:
                return jsonify({"message": "JSON requerido"}), 400

            data = request.get_json()
            title = data.get("title")

            if not title:
                return jsonify({"message": "Título é obrigatório"}), 400

            task = Task(
                title=title,
                description=data.get("description", ""),
                priority=data.get("priority", "Média"),
                status=data.get("status", "Pendente"),
                user_id=user_id
            )

            db.session.add(task)
            db.session.commit()

            return jsonify(task.to_dict()), 201

        except Exception as e:
            db.session.rollback()
            print("\n=== ERRO AO CRIAR TAREFA ===")
            print(e)
            traceback.print_exc()
            print("============================\n")
            return jsonify({"message": "Erro ao criar tarefa"}), 500

    # ======================================================
    # LIST TASKS
    # ======================================================
    @app.route("/api/tasks", methods=["GET"])
    @jwt_required()
    def get_tasks():
        try:
            user_id = int(get_jwt_identity())

            tasks = Task.query.filter_by(user_id=user_id).all()
            return jsonify([t.to_dict() for t in tasks]), 200

        except Exception as e:
            print("\n=== ERRO AO LISTAR TAREFAS ===")
            print(e)
            traceback.print_exc()
            print("===============================\n")
            return jsonify({"message": "Erro ao buscar tarefas"}), 500

    # ======================================================
    # UPDATE TASK
    # ======================================================
    @app.route("/api/tasks/<int:task_id>", methods=["PUT"])
    @jwt_required()
    def update_task(task_id):
        try:
            user_id = int(get_jwt_identity())

            task = Task.query.filter_by(id=task_id, user_id=user_id).first()

            if not task:
                return jsonify({"message": "Tarefa não encontrada"}), 404

            data = request.get_json()

            task.title = data.get("title", task.title)
            task.description = data.get("description", task.description)
            task.priority = data.get("priority", task.priority)
            task.status = data.get("status", task.status)

            db.session.commit()
            return jsonify(task.to_dict()), 200

        except Exception as e:
            db.session.rollback()
            print("\n=== ERRO AO ATUALIZAR TAREFA ===")
            print(e)
            traceback.print_exc()
            print("=================================\n")
            return jsonify({"message": "Erro ao atualizar tarefa"}), 500

    # ======================================================
    # DELETE TASK
    # ======================================================
    @app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
    @jwt_required()
    def delete_task(task_id):
        try:
            user_id = int(get_jwt_identity())

            task = Task.query.filter_by(id=task_id, user_id=user_id).first()

            if not task:
                return jsonify({"message": "Tarefa não encontrada"}), 404

            db.session.delete(task)
            db.session.commit()

            return jsonify({"message": "Tarefa excluída"}), 200

        except Exception as e:
            db.session.rollback()
            print("\n=== ERRO AO EXCLUIR TAREFA ===")
            print(e)
            traceback.print_exc()
            print("================================\n")
            return jsonify({"message": "Erro ao excluir tarefa"}), 500
