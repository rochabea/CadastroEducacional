from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import unittest
import time

class TestSistemaAvaliacao(unittest.TestCase):
    def setUp(self):
        # Configurar o Chrome em modo headless
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Inicializar o driver
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.driver.implicitly_wait(10)
        self.base_url = "http://localhost:8000"

    def tearDown(self):
        self.driver.quit()

    def test_cadastro_aluno(self):
        """CT01 - Testar o cadastro de um novo aluno no sistema"""
        self.driver.get(f"{self.base_url}/cadastro/aluno/")
        
        # Preencher formulário
        nome = self.driver.find_element(By.NAME, "nome")
        matricula = self.driver.find_element(By.NAME, "matricula")
        username = self.driver.find_element(By.NAME, "username")
        password = self.driver.find_element(By.NAME, "password")
        
        nome.send_keys("AnaBia")
        matricula.send_keys("20230120")
        username.send_keys("ana.bia")
        password.send_keys("senha123")
        
        # Submeter formulário
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Verificar redirecionamento e mensagem de sucesso
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/login/")
        )
        
        # Fazer login para verificar se o aluno foi cadastrado
        username_login = self.driver.find_element(By.NAME, "username")
        password_login = self.driver.find_element(By.NAME, "password")
        
        username_login.send_keys("ana.bia")
        password_login.send_keys("senha123")
        
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        # Verificar se foi redirecionado para o dashboard do aluno
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/dashboard/aluno/")
        )

    def test_cadastro_professor(self):
        """CT02 - Testar o cadastro de um novo professor no sistema"""
        self.driver.get(f"{self.base_url}/cadastro/professor/")
        
        # Preencher formulário
        nome = self.driver.find_element(By.NAME, "nome")
        username = self.driver.find_element(By.NAME, "username")
        password = self.driver.find_element(By.NAME, "password")
        
        nome.send_keys("Maria Oliveira")
        username.send_keys("maria.oliveira")
        password.send_keys("senha123")
        
        # Submeter formulário
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Verificar redirecionamento e mensagem de sucesso
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/login/")
        )
        
        # Fazer login para verificar se o professor foi cadastrado
        username_login = self.driver.find_element(By.NAME, "username")
        password_login = self.driver.find_element(By.NAME, "password")
        
        username_login.send_keys("maria.oliveira")
        password_login.send_keys("senha123")
        
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        # Verificar se foi redirecionado para o dashboard do professor
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/dashboard/professor/")
        )

    def test_cadastro_avaliacao(self):
        """CT03 - Testar o cadastro de uma nova avaliação"""
        # Primeiro fazer login como professor
        self.driver.get(f"{self.base_url}/login/")
        username = self.driver.find_element(By.NAME, "username")
        password = self.driver.find_element(By.NAME, "password")
        
        username.send_keys("maria.oliveira")
        password.send_keys("senha123")
        
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        # Ir para a página de lançar avaliação
        self.driver.get(f"{self.base_url}/lancar-avaliacao/")
        
        # Preencher o formulário
        aluno_select = Select(self.driver.find_element(By.NAME, "aluno"))
        nota_b1 = self.driver.find_element(By.NAME, "nota_b1")
        nota_b2 = self.driver.find_element(By.NAME, "nota_b2")
        faltas = self.driver.find_element(By.NAME, "faltas")
        
        aluno_select.select_by_visible_text("AnaBia")
        nota_b1.send_keys("7.5")
        nota_b2.send_keys("8.0")
        faltas.send_keys("5")
        
        # Enviar o formulário
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Verificar se foi redirecionado para o dashboard
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/dashboard/professor/")
        )
        
        # Verificar se a avaliação aparece na listagem
        self.assertTrue(self.driver.find_element(By.XPATH, "//td[contains(text(), '7.75')]"))
        self.assertTrue(self.driver.find_element(By.XPATH, "//td[contains(text(), 'Aprovado')]"))

    def test_calculo_media(self):
        """CT04 - Verificar o cálculo automático da média"""
        # Primeiro fazer login como professor
        self.driver.get(f"{self.base_url}/login/")
        username = self.driver.find_element(By.NAME, "username")
        password = self.driver.find_element(By.NAME, "password")
        
        username.send_keys("maria.oliveira")
        password.send_keys("senha123")
        
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        # Ir para a página de lançar avaliação
        self.driver.get(f"{self.base_url}/lancar-avaliacao/")
        
        # Preencher o formulário
        aluno_select = Select(self.driver.find_element(By.NAME, "aluno"))
        nota_b1 = self.driver.find_element(By.NAME, "nota_b1")
        nota_b2 = self.driver.find_element(By.NAME, "nota_b2")
        faltas = self.driver.find_element(By.NAME, "faltas")
        
        aluno_select.select_by_visible_text("AnaBia")
        nota_b1.send_keys("5.0")
        nota_b2.send_keys("7.0")
        faltas.send_keys("2")
        
        # Enviar o formulário
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Verificar se a média foi calculada corretamente
        self.assertTrue(self.driver.find_element(By.XPATH, "//td[contains(text(), '6.0')]"))

    def test_calculo_status(self):
        """CT05 - Verificar o cálculo automático do status"""
        # Primeiro fazer login como professor
        self.driver.get(f"{self.base_url}/login/")
        username = self.driver.find_element(By.NAME, "username")
        password = self.driver.find_element(By.NAME, "password")
        
        username.send_keys("maria.oliveira")
        password.send_keys("senha123")
        
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        # Ir para a página de lançar avaliação
        self.driver.get(f"{self.base_url}/lancar-avaliacao/")
        
        # Preencher o formulário
        aluno_select = Select(self.driver.find_element(By.NAME, "aluno"))
        nota_b1 = self.driver.find_element(By.NAME, "nota_b1")
        nota_b2 = self.driver.find_element(By.NAME, "nota_b2")
        faltas = self.driver.find_element(By.NAME, "faltas")
        
        aluno_select.select_by_visible_text("AnaBia")
        nota_b1.send_keys("6.0")
        nota_b2.send_keys("6.0")
        faltas.send_keys("11")
        
        # Enviar o formulário
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Verificar se o status foi calculado corretamente
        self.assertTrue(self.driver.find_element(By.XPATH, "//td[contains(text(), 'Reprovado')]"))

    def test_consulta_avaliacoes_aluno(self):
        """CT06 - Testar a consulta de avaliações por aluno"""
        # Primeiro fazer login como aluno
        self.driver.get(f"{self.base_url}/login/")
        username = self.driver.find_element(By.NAME, "username")
        password = self.driver.find_element(By.NAME, "password")
        
        username.send_keys("ana.bia")
        password.send_keys("senha123")
        
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        # Ir para a página do boletim
        self.driver.get(f"{self.base_url}/boletim/")
        
        # Verificar se os elementos do boletim estão presentes
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, "boletim-info"))
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, "aluno-info"))
        
        # Verificar se as avaliações estão listadas
        self.assertTrue(self.driver.find_element(By.TAG_NAME, "table"))

    def test_validacao_matricula_unica(self):
        """CT07 - Verificar validação de matrícula única"""
        self.driver.get(f"{self.base_url}/cadastro/aluno/")
        
        # Preencher formulário com matrícula existente
        nome = self.driver.find_element(By.NAME, "nome")
        matricula = self.driver.find_element(By.NAME, "matricula")
        username = self.driver.find_element(By.NAME, "username")
        password = self.driver.find_element(By.NAME, "password")
        
        nome.send_keys("Novo Aluno")
        matricula.send_keys("2023001")  # Matrícula já existente
        username.send_keys("novo.aluno")
        password.send_keys("senha123")
        
        # Submeter formulário
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Verificar mensagem de erro
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, "alert-error"))
        self.assertTrue("matrícula já existe" in self.driver.page_source.lower())

    def test_validacao_notas(self):
        """CT08 - Verificar validação de notas"""
        # Primeiro fazer login como professor
        self.driver.get(f"{self.base_url}/login/")
        username = self.driver.find_element(By.NAME, "username")
        password = self.driver.find_element(By.NAME, "password")
        
        username.send_keys("maria.oliveira")
        password.send_keys("senha123")
        
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        # Ir para a página de lançar avaliação
        self.driver.get(f"{self.base_url}/lancar-avaliacao/")
        
        # Preencher o formulário com notas inválidas
        aluno_select = Select(self.driver.find_element(By.NAME, "aluno"))
        nota_b1 = self.driver.find_element(By.NAME, "nota_b1")
        nota_b2 = self.driver.find_element(By.NAME, "nota_b2")
        faltas = self.driver.find_element(By.NAME, "faltas")
        
        aluno_select.select_by_visible_text("AnaBia")
        nota_b1.send_keys("-1.0")
        nota_b2.send_keys("11.0")
        faltas.send_keys("2")
        
        # Enviar o formulário
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Verificar mensagem de erro
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, "alert-error"))
        self.assertTrue("notas devem estar entre 0 e 10" in self.driver.page_source.lower())

if __name__ == "__main__":
    unittest.main() 