from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    """Page Object para a tela de Login (login.html)"""
    
    URL_PATH = "/login.html"
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "#login-form .btn")
    ERROR_MESSAGE = (By.ID, "error-message")

    def open(self):
        """Abre a página de login."""
        self.open_url(self.URL_PATH)

    def login(self, email, password):
        """Preenche o formulário de login e envia."""
        self.type_into(self.EMAIL_INPUT, email)
        self.type_into(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        
    def get_error_message(self):
        """Retorna a mensagem de erro da tela."""
        return self.get_text(self.ERROR_MESSAGE)