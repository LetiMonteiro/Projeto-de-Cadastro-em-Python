import json
import re
from datetime import datetime
import getpass

class SistemaCadastro:
    def __init__(self, arquivo_usuarios='usuarios.json'):
        self.arquivo_usuarios = arquivo_usuarios
        self.usuarios = self.carregar_usuarios()

    def carregar_usuarios(self):
        """Carrega os usuários do arquivo JSON"""
        try:
            with open(self.arquivo_usuarios, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def salvar_usuarios(self):
        """Salva os usuários no arquivo JSON"""
        with open(self.arquivo_usuarios, 'w') as f:
            json.dump(self.usuarios, f, indent=4)

    def validar_email(self, email):
        """Valida o formato do email"""
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(padrao, email) is not None

    def validar_senha(self, senha):
        """Valida a força da senha"""
        if len(senha) < 8:
            return False, "A senha deve ter pelo menos 8 caracteres"

        if not any(c.isupper() for c in senha):
            return False, "A senha deve conter pelo menos uma letra maiúscula"

        if not any(c.islower() for c in senha):
            return False, "A senha deve conter pelo menos uma letra minúscula"

        if not any(c.isdigit() for c in senha):
            return False, "A senha deve conter pelo menos um número"

        return True, "Senha válida"

    def email_existe(self, email):
        """Verifica se o email já está cadastrado"""
        return any(usuario['email'] == email for usuario in self.usuarios)

    def cadastrar_usuario(self):
        """Realiza o cadastro de um novo usuário"""
        print("\n" + "="*50)
        print("          CADASTRO DE USUÁRIO")
        print("="*50)

        # Nome
        while True:
            nome = input("Nome completo: ").strip()
            if len(nome) < 3:
                print("Nome deve ter pelo menos 3 caracteres.")
            else:
                break

        # Email
        while True:
            email = input("Email: ").strip().lower()
            if not self.validar_email(email):
                print("Email inválido. Digite um email válido.")
            elif self.email_existe(email):
                print("Este email já está cadastrado.")
            else:
                break

        # Senha
        while True:
            senha = getpass.getpass("Senha: ")
            senha_valida, mensagem = self.validar_senha(senha)
            if not senha_valida:
                print(f"Senha inválida: {mensagem}")
                continue

            confirmar_senha = getpass.getpass("Confirmar senha: ")
            if senha != confirmar_senha:
                print("As senhas não coincidem.")
            else:
                break

        # Telefone (opcional)
        telefone = input("Telefone (opcional): ").strip()
        telefone = telefone if telefone else None

        # Data de nascimento (opcional)
        data_nascimento = input("Data de nascimento (DD/MM/AAAA - opcional): ").strip()
        data_nascimento = data_nascimento if data_nascimento else None

        # Criar usuário
        usuario = {
            'id': len(self.usuarios) + 1,
            'nome': nome,
            'email': email,
            'senha': senha,
            'telefone': telefone,
            'data_nascimento': data_nascimento,
            'data_cadastro': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'ativo': True
        }

        self.usuarios.append(usuario)
        self.salvar_usuarios()

        print("\n✅ Cadastro realizado com sucesso!")
        print(f"Bem-vindo(a), {nome}!")
        return usuario

    def listar_usuarios(self):
        """Lista todos os usuários cadastrados"""
        print("\n" + "="*50)
        print("          LISTA DE USUÁRIOS")
        print("="*50)

        if not self.usuarios:
            print("Nenhum usuário cadastrado.")
            return

        for usuario in self.usuarios:
            status = "✅ Ativo" if usuario['ativo'] else "❌ Inativo"
            print(f"ID: {usuario['id']}")
            print(f"Nome: {usuario['nome']}")
            print(f"Email: {usuario['email']}")
            print(f"Telefone: {usuario['telefone'] or 'Não informado'}")
            print(f"Data Cadastro: {usuario['data_cadastro']}")
            print(f"Status: {status}")
            print("-" * 30)

    def buscar_usuario(self, email):
        """Busca um usuário pelo email"""
        for usuario in self.usuarios:
            if usuario['email'] == email:
                return usuario
        return None

    def menu_principal(self):
        """Menu principal do sistema"""
        while True:
            print("\n" + "="*50)
            print("          SISTEMA DE CADASTRO")
            print("="*50)
            print("1. Cadastrar novo usuário")
            print("2. Listar todos os usuários")
            print("3. Buscar usuário por email")
            print("4. Sair")
            print("="*50)

            opcao = input("Escolha uma opção: ").strip()

            if opcao == '1':
                self.cadastrar_usuario()
            elif opcao == '2':
                self.listar_usuarios()
            elif opcao == '3':
                email = input("Digite o email para buscar: ").strip().lower()
                usuario = self.buscar_usuario(email)
                if usuario:
                    print(f"\nUsuário encontrado:")
                    print(f"Nome: {usuario['nome']}")
                    print(f"Email: {usuario['email']}")
                    print(f"Telefone: {usuario['telefone'] or 'Não informado'}")
                else:
                    print("Usuário não encontrado.")
            elif opcao == '4':
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida. Tente novamente.")

# Executar o sistema
if __name__ == "__main__":
    sistema = SistemaCadastro()
    sistema.menu_principal()