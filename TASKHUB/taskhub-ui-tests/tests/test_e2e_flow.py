import pytest
from faker import Faker
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from pages.tasks_page import TasksPage

# Inicializa o Faker para gerar dados aleatórios
fake = Faker('pt_BR')

@pytest.mark.usefixtures("driver")
class TestE2EFlow:
    
    def test_full_user_flow(self, driver):
        """
        Testa o fluxo completo:
        1. Cadastro de novo usuário
        2. Login
        3. Criação de tarefa
        4. Edição de tarefa
        5. Exclusão de tarefa
        """
        
        # Prepara as páginas
        signup_page = SignupPage(driver)
        login_page = LoginPage(driver)
        tasks_page = TasksPage(driver)
        
        # Gera dados únicos para o novo usuário
        user_name = fake.name()
        user_email = fake.email()
        user_pass = "senha@Forte123"
        
        # --- 1. Cadastro ---
        print(f"Testando Cadastro com: {user_email}")
        signup_page.open()
        signup_page.register_user(user_name, user_email, user_pass)
        
        # --- 2. Login ---
        # (O cadastro bem-sucedido redireciona para o login)
        print("Testando Login...")
        
        # Espera o navegador ser redirecionado para a página de login
        assert login_page.is_visible(login_page.LOGIN_BUTTON, timeout=15)
        
        login_page.login(user_email, user_pass)
        
        # Verifica se o login foi bem-sucedido
        assert tasks_page.is_logged_in(), "Login falhou, botão 'Sair' não encontrado."
        
        # --- 3. Criação de Tarefa ---
        print("Testando Criação de Tarefa...")
        task_title = "Minha Tarefa de Teste"
        task_desc = "Descrição da tarefa."
        
        tasks_page.create_task(task_title, task_desc)
        
        # Verifica se a tarefa apareceu na lista
        assert tasks_page.get_first_task_title() == task_title

        # --- 4. Edição de Tarefa ---
        print("Testando Edição de Tarefa...")
        edited_title = "Tarefa Editada"
        edited_desc = "Descrição atualizada."
        
        tasks_page.edit_first_task(edited_title, edited_desc)
        
        # Verifica se o título foi atualizado
        assert tasks_page.get_first_task_title() == edited_title
        
        # --- 5. Exclusão de Tarefa ---
        print("Testando Exclusão de Tarefa...")
        tasks_page.delete_first_task()
        
        # Verifica se a lista de tarefas está vazia
        assert tasks_page.is_task_list_empty(), "A lista de tarefas não ficou vazia."
        
        print("Fluxo E2E (ponta-a-ponta) concluído com sucesso!")