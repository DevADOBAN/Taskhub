from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class SignupPage(BasePage):
    """Page Object para a tela de Cadastro (signup.html)"""
    
    # Locators 
    URL_PATH = "/signup.html"
    NAME_INPUT = (By.ID, "name")
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    SIGNUP_BUTTON = (By.CSS_SELECTOR, "#signup-form .btn")
    LOGIN_LINK = (By.LINK_TEXT, "Faça login")

    def open(self):
        """Abre a página de cadastro."""
        self.open_url(self.URL_PATH)

    def register_user(self, name, email, password):
        """Preenche o formulário de cadastro e envia."""
        self.type_into(self.NAME_INPUT, name)
        self.type_into(self.EMAIL_INPUT, email)
        self.type_into(self.PASSWORD_INPUT, password)

        self.click(self.SIGNUP_BUTTON)
