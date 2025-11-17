from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:
    """
    Classe base para todas as Páginas (Page Objects).
    Contém métodos utilitários comuns.
    """
    
    def __init__(self, driver, base_url="http://127.0.0.1:5000/"):
        self.driver = driver
        self.base_url = base_url

    def open_url(self, path):
        """Abre uma URL relativa (ex: /login.html)"""
        self.driver.get(f"{self.base_url}{path}")

    def find_element(self, locator, timeout=10):
        """
        Encontra e retorna um elemento, esperando até que ele esteja visível.
        'locator' deve ser uma tupla (ex: (By.ID, "meu_id"))
        """
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            raise Exception(f"Elemento não encontrado ou visível: {locator}")

    def type_into(self, locator, text):
        """Digita um texto em um campo."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def click(self, locator):
        """Clica em um elemento."""
        element = self.find_element(locator)
        element.click()
        
    def get_text(self, locator):
        """Pega o texto de um elemento."""
        element = self.find_element(locator)
        return element.text

    def is_visible(self, locator, timeout=5):
        """Verifica se um elemento está visível."""
        try:
            self.find_element(locator, timeout)
            return True
        except:
            return False