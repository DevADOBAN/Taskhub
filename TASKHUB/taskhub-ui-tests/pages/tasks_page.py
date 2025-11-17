from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class TasksPage(BasePage):
    """Page Object para a tela de Tarefas (tasks.html)"""
    
    # Locators
    LOGOUT_BUTTON = (By.ID, "logout-btn")
    ADD_TASK_BUTTON = (By.ID, "add-task-btn")
    
    # Locators do Modal
    MODAL = (By.ID, "task-modal")
    TITLE_INPUT = (By.ID, "title")
    DESCRIPTION_INPUT = (By.ID, "description")
    SAVE_BUTTON = (By.CSS_SELECTOR, "#task-form .btn")
    
    # Locators da Lista de Tarefas
    TASK_LIST = (By.ID, "task-list")
    FIRST_TASK_TITLE = (By.CSS_SELECTOR, "#task-list .task-item:first-child h3")
    FIRST_TASK_EDIT_BTN = (By.CSS_SELECTOR, "#task-list .task-item:first-child .edit-btn")
    FIRST_TASK_DELETE_BTN = (By.CSS_SELECTOR, "#task-list .task-item:first-child .delete-btn")
    NO_TASKS_MESSAGE = (By.XPATH, "//div[@id='task-list']/p[text()='Você ainda não tem tarefas.']")

    def is_logged_in(self, timeout=10):
        """Verifica se o botão 'Sair' está visível, indicando login."""
        return self.is_visible(self.LOGOUT_BUTTON, timeout)

    def create_task(self, title, description):
        """Abre o modal, preenche e salva uma nova tarefa."""
        self.click(self.ADD_TASK_BUTTON)
        self.find_element(self.MODAL) # Espera o modal aparecer
        self.type_into(self.TITLE_INPUT, title)
        self.type_into(self.DESCRIPTION_INPUT, description)
        self.click(self.SAVE_BUTTON)
        
    def get_first_task_title(self):
        """Pega o título da primeira tarefa da lista."""
        return self.get_text(self.FIRST_TASK_TITLE)
        
    def edit_first_task(self, new_title, new_description):
        """Clica em editar na primeira tarefa, muda e salva."""
        self.click(self.FIRST_TASK_EDIT_BTN)
        self.find_element(self.MODAL) # Espera o modal
        self.type_into(self.TITLE_INPUT, new_title)
        self.type_into(self.DESCRIPTION_INPUT, new_description)
        self.click(self.SAVE_BUTTON)
        
    def delete_first_task(self):
        """Clica em deletar na primeira tarefa e confirma."""
        self.click(self.FIRST_TASK_DELETE_BTN)
        
        # O Selenium precisa lidar com o 'alert' do navegador
        alert = self.driver.switch_to.alert
        alert.accept() # Clica em "OK" no alerta

    def is_task_list_empty(self):
        """Verifica se a mensagem 'Você ainda não tem tarefas' está visível."""
        return self.is_visible(self.NO_TASKS_MESSAGE)