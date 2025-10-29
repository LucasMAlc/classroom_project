"""
Script de testes da API
Execute: python test_api_completo.py
"""

import requests

BASE_URL = "http://127.0.0.1:8000/api"


class APITester:
    def __init__(self):
        self.admin_token = None
        self.aluno_token = None
        self.passed = 0
        self.failed = 0
    
    def test(self, name, condition):
        if condition:
            self.passed += 1
            print(f"[PASS] {name}")
        else:
            self.failed += 1
            print(f"[FAIL] {name}")
        return condition
    
    def section(self, title):
        print(f"\n{'='*50}")
        print(f"{title}")
        print('='*50)
    
    def test_authentication(self):
        self.section("AUTENTICACAO")
        
        # Admin
        response = requests.post(
            f"{BASE_URL}/token/",
            json={"username": "admin", "password": "admin123"}
        )
        if self.test("Login Admin", response.status_code == 200):
            self.admin_token = response.json()['access']
        
        # Aluno
        response = requests.post(
            f"{BASE_URL}/token/",
            json={"username": "joao", "password": "senha123"}
        )
        if self.test("Login Aluno", response.status_code == 200):
            self.aluno_token = response.json()['access']
    
    def test_endpoints(self):
        self.section("ENDPOINTS")
        
        admin_headers = {"Authorization": f"Bearer {self.admin_token}"}
        aluno_headers = {"Authorization": f"Bearer {self.aluno_token}"}
        
        # Admin
        self.test("GET /treinamentos/", 
                 requests.get(f"{BASE_URL}/treinamentos/", headers=admin_headers).status_code == 200)
        self.test("GET /turmas/", 
                 requests.get(f"{BASE_URL}/turmas/", headers=admin_headers).status_code == 200)
        self.test("GET /recursos/", 
                 requests.get(f"{BASE_URL}/recursos/", headers=admin_headers).status_code == 200)
        
        # Aluno
        self.test("GET /meus-dados/", 
                 requests.get(f"{BASE_URL}/meus-dados/", headers=aluno_headers).status_code == 200)
        self.test("GET /minhas-turmas/", 
                 requests.get(f"{BASE_URL}/minhas-turmas/", headers=aluno_headers).status_code == 200)
    
    def test_business_rules(self):
        self.section("REGRAS DE NEGOCIO")
        
        headers = {"Authorization": f"Bearer {self.aluno_token}"}
        response = requests.get(f"{BASE_URL}/minhas-turmas/", headers=headers)
        
        if response.status_code == 200:
            turmas = response.json()
            turma_futura = next((t for t in turmas if not t['pode_acessar']), None)
            
            if turma_futura:
                self.test("Turma futura - acesso previo", len(turma_futura['recursos']) == 2)
            
            self.test("Campo pode_acessar presente", 
                     all('pode_acessar' in t for t in turmas))
    
    def test_security(self):
        self.section("SEGURANCA")
        
        # Sem token
        self.test("Bloqueia sem token", 
                 requests.get(f"{BASE_URL}/treinamentos/").status_code == 401)
        
        # Aluno criar treinamento
        headers = {"Authorization": f"Bearer {self.aluno_token}"}
        self.test("Aluno nao cria treinamento",
                 requests.post(f"{BASE_URL}/treinamentos/", 
                              headers=headers, 
                              json={"nome": "Test", "descricao": "Test"}).status_code == 403)
    
    def run(self):
        print("\n" + "="*50)
        print("TESTES DA API - CLASSROOM PROJECT")
        print("="*50)
        
        try:
            self.test_authentication()
            if self.admin_token and self.aluno_token:
                self.test_endpoints()
                self.test_business_rules()
                self.test_security()
            
            # Resumo
            print(f"\n{'='*50}")
            print("RESUMO")
            print('='*50)
            total = self.passed + self.failed
            print(f"Passou: {self.passed}")
            print(f"Falhou: {self.failed}")
            print(f"Total: {total}")
            
        except requests.exceptions.ConnectionError:
            print("\n[ERRO] Servidor nao esta rodando")
            print("Execute: python manage.py runserver")


if __name__ == "__main__":
    tester = APITester()
    tester.run()