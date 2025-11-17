# app/routes.py
from flask import request, jsonify
from app import db, bcrypt
from app.models import User, Task
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.exc import SQLAlchemyError


def init_routes(app):

    # =============================
    # AUTH: SIGNUP
    # =============================
    @app.route('/auth/signup', methods=['POST'])
    def signup():
        if not request.is_json:
            return jsonify({"message": "JSON requerido"}), 400

        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"message": "Email e senha são obrigatórios"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"message": "Usuário já cadastrado"}), 409

        try:
            hashed = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(
                email=email,
                name=data.get('name') or email.split('@')[0],
                password_hash=hashed
            )
            db.session.add(new_user)
            db.session.commit()
            return jsonify({
                "message": "Usuário criado com sucesso",
                "userId": new_user.id
            }), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"message": "Erro ao criar usuário"}), 500


    # =============================
    # AUTH: LOGIN
    # =============================
    @app.route('/auth/login', methods=['POST'])
    def login():
        if not request.is_json:
            return jsonify({"message": "JSON requerido"}), 400

        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"message": "Email e senha são obrigatórios"}), 400

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            token = create_access_token(identity=user.id)
            return jsonify(access_token=token), 200
        else:
            return jsonify({"message": "Credenciais inválidas"}), 401


    # =============================
    # USER: ME
    # =============================
    @app.route('/me', methods=['GET'])
    @jwt_required()
    def get_me():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "Usuário não encontrado"}), 404
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email
        })


    # =============================
    # TASKS: CREATE
    # =============================
    @app.route('/tasks', methods=['POST'])
    @jwt_required()
    def create_task():
        user_id = get_jwt_identity()
        if not request.is_json:
            return jsonify({"message": "JSON requerido"}), 400

        data = request.get_json()
        title = data.get('title')

        if not title:
            return jsonify({"message": "Título é obrigatório"}), 400

        try:
            task = Task(
                title=title,
                description=data.get('description', ''),
                priority=data.get('priority', 'Média'),
                status=data.get('status', 'Pendente'),
                user_id=user_id
            )
            db.session.add(task)
            db.session.commit()
            return jsonify(task.to_dict()), 201
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"message": "Erro ao criar tarefa"}), 500


    # =============================
    # TASKS: LIST
    # =============================
    @app.route('/tasks', methods=['GET'])
    @jwt_required()
    def get_tasks():
        user_id = get_jwt_identity()
        tasks = Task.query.filter_by(user_id=user_id).all()
        return jsonify([t.to_dict() for t in tasks])


    # =============================
    # TASKS: GET BY ID
    # =============================
    @app.route('/tasks/<int:task_id>', methods=['GET'])
    @jwt_required()
    def get_task_by_id(task_id):
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return jsonify({"message": "Tarefa não encontrada"}), 404
        return jsonify(task.to_dict())


    # =============================
    # TASKS: UPDATE
    # =============================
    @app.route('/tasks/<int:task_id>', methods=['PUT'])
    @jwt_required()
    def update_task(task_id):
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return jsonify({"message": "Tarefa não encontrada"}), 404

        if not request.is_json:
            return jsonify({"message": "JSON requerido"}), 400

        data = request.get_json()

        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.priority = data.get('priority', task.priority)
        task.status = data.get('status', task.status)

        try:
            db.session.commit()
            return jsonify(task.to_dict())
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"message": "Erro ao atualizar tarefa"}), 500


    # =============================
    # TASKS: DELETE
    # =============================
    @app.route('/tasks/<int:task_id>', methods=['DELETE'])
    @jwt_required()
    def delete_task(task_id):
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return jsonify({"message": "Tarefa não localizada"}), 404

        try:
            db.session.delete(task)
            db.session.commit()
            return jsonify({"message": "Tarefa excluída com sucesso"}), 200
        except SQLAlchemyError:
            db.session.rollback()
            return jsonify({"message": "Erro ao excluir tarefa"}), 500