import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def driver():
    """
    Fixture do Pytest para configurar e fornecer o driver do Selenium.
    """
    # Configura o serviço do Chrome usando o webdriver-manager
    # Isso baixa e instala o driver correto automaticamente
    service = Service(ChromeDriverManager().install())
    
    
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Descomente para rodar sem abrir a janela
    options.add_argument("--start-maximized")
    
    # Inicializa o driver
    driver = webdriver.Chrome(service=service, options=options)
    
    # "Entrega" o driver para o teste
    yield driver
    
    # Código de "limpeza" (executa após o teste terminar)
    print("\nFechando o navegador...")

    driver.quit()
