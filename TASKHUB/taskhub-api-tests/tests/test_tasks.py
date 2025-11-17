import json

def test_create_task_success(authenticated_client):
    """
    Testa a criação de uma nova tarefa com sucesso.
    """
    client = authenticated_client['client']
    token = authenticated_client['token']
    
    task_data = {
        "title": "Minha Primeira Tarefa",
        "description": "Descrição da tarefa de teste.",
        "priority": "Alta",
        "status": "Pendente"
    }
    
    # Envia o token no cabeçalho de autorização
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = client.post('/tasks', data=json.dumps(task_data), headers=headers)
    
    assert response.status_code == 201
    assert response.json['title'] == "Minha Primeira Tarefa"
    assert response.json['priority'] == "Alta"

def test_get_tasks_success(authenticated_client):
    """
    Testa se o GET /tasks retorna uma lista de tarefas do usuário.
    """
    client = authenticated_client['client']
    token = authenticated_client['token']
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    # Cria uma tarefa primeiro
    client.post('/tasks', data=json.dumps({"title": "Tarefa A"}), headers=headers)
    
    # Busca a lista de tarefas
    response = client.get('/tasks', headers=headers)
    
    assert response.status_code == 200
    assert isinstance(response.json, list) # Deve ser uma lista
    assert len(response.json) == 1
    assert response.json[0]['title'] == "Tarefa A"

def test_get_task_by_id(authenticated_client):
    """
    Testa o GET /tasks/:id para buscar uma tarefa específica.
    """
    client = authenticated_client['client']
    token = authenticated_client['token']
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

    # Cria a tarefa
    create_response = client.post('/tasks', data=json.dumps({"title": "Tarefa Específica"}), headers=headers)
    task_id = create_response.json['id']
    
    # Busca a tarefa pelo ID
    response = client.get(f'/tasks/{task_id}', headers=headers)
    
    assert response.status_code == 200
    assert response.json['title'] == "Tarefa Específica"
    
    # Testa buscar um ID que não existe
    response_fail = client.get('/tasks/9999', headers=headers)
    assert response_fail.status_code == 404

def test_update_task(authenticated_client):
    """
    Testa o PUT /tasks/:id para atualizar uma tarefa.
    """
    client = authenticated_client['client']
    token = authenticated_client['token']
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

    # Cria a tarefa
    create_response = client.post('/tasks', data=json.dumps({"title": "Original"}), headers=headers)
    task_id = create_response.json['id']

    # Atualiza a tarefa
    update_data = {"title": "Título Atualizado", "status": "Concluída"}
    response = client.put(f'/tasks/{task_id}', data=json.dumps(update_data), headers=headers)
    
    assert response.status_code == 200
    assert response.json['title'] == "Título Atualizado"
    assert response.json['status'] == "Concluída"

def test_delete_task(authenticated_client):
    """
    Testa o DELETE /tasks/:id para excluir uma tarefa.
    """
    client = authenticated_client['client']
    token = authenticated_client['token']
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    # Cria a tarefa
    create_response = client.post('/tasks', data=json.dumps({"title": "Para Deletar"}), headers=headers)
    task_id = create_response.json['id']
    
    # Deleta a tarefa
    delete_response = client.delete(f'/tasks/{task_id}', headers=headers)
    assert delete_response.status_code == 200
    assert "Tarefa deletada" in delete_response.json['message']
    
    # Tenta buscar a tarefa deletada
    get_response = client.get(f'/tasks/{task_id}', headers=headers)
    assert get_response.status_code == 404 # Deve falhar (Não Encontrado)

def test_task_access_unauthorized(client, fresh_db):
    """
    Testa se um usuário sem token não pode acessar as rotas de tarefas.
    """
    # Tenta acessar sem token
    response = client.get('/tasks')
    assert response.status_code == 401 # Unauthorized
    
    response = client.post('/tasks', data=json.dumps({"title": "Tarefa"}))
    assert response.status_code == 401 # Unauthorized