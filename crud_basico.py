import json
import os
import re
import hashlib

ARQUIVO = "usuarios.json"

# ---------- UTILIDADES ----------

def carregar_dados():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_dados(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def email_valido(email):
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(padrao, email)

# ---------- CLASSES ----------

class Usuario:
    def __init__(self, id, nome, email, senha_hash):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha_hash
        }

class UsuarioCRUD:
    def __init__(self):
        self.usuarios = carregar_dados()
        self.proximo_id = self._gerar_proximo_id()

    def _gerar_proximo_id(self):
        if not self.usuarios:
            return 1
        return max(u["id"] for u in self.usuarios) + 1

    def cadastrar(self):
        nome = input("Nome: ")
        email = input("Email: ")

        if not email_valido(email):
            print("❌ Email inválido.")
            return

        if any(u["email"] == email for u in self.usuarios):
            print("❌ Email já cadastrado.")
            return

        senha = input("Senha: ")
        senha_hash = hash_senha(senha)

        usuario = Usuario(self.proximo_id, nome, email, senha_hash)
        self.usuarios.append(usuario.to_dict())
        salvar_dados(self.usuarios)

        self.proximo_id += 1
        print("✅ Usuário cadastrado com sucesso!")

    def listar(self):
        if not self.usuarios:
            print("⚠️ Nenhum usuário cadastrado.")
            return

        for u in self.usuarios:
            print(f"ID: {u['id']} | Nome: {u['nome']} | Email: {u['email']}")

    def atualizar(self):
        id_busca = int(input("ID do usuário: "))

        for u in self.usuarios:
            if u["id"] == id_busca:
                u["nome"] = input("Novo nome: ")
                salvar_dados(self.usuarios)
                print("✏️ Usuário atualizado.")
                return

        print("❌ Usuário não encontrado.")

    def deletar(self):
        id_busca = int(input("ID do usuário: "))

        for u in self.usuarios:
            if u["id"] == id_busca:
                self.usuarios.remove(u)
                salvar_dados(self.usuarios)
                print("🗑️ Usuário removido.")
                return

        print("❌ Usuário não encontrado.")

    def login(self):
        email = input("Email: ")
        senha = input("Senha: ")
        senha_hash = hash_senha(senha)

        for u in self.usuarios:
            if u["email"] == email and u["senha"] == senha_hash:
                print(f"\n✅ Login realizado! Bem-vinda, {u['nome']} 💙")
                return True

        print("❌ Email ou senha inválidos.")
        return False

# ---------- MENUS ----------

def menu_principal():
    crud = UsuarioCRUD()

    while True:
        print("\n===== SISTEMA =====")
        print("1 - Cadastrar")
        print("2 - Login")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            crud.cadastrar()
        elif opcao == "2":
            if crud.login():
                menu_usuario(crud)
        elif opcao == "0":
            print("👋 Saindo...")
            break
        else:
            print("❌ Opção inválida.")

def menu_usuario(crud):
    while True:
        print("\n===== MENU USUÁRIO =====")
        print("1 - Listar usuários")
        print("2 - Atualizar usuário")
        print("3 - Deletar usuário")
        print("0 - Logout")

        opcao = input("Escolha: ")

        if opcao == "1":
            crud.listar()
        elif opcao == "2":
            crud.atualizar()
        elif opcao == "3":
            crud.deletar()
        elif opcao == "0":
            print("🔒 Logout realizado.")
            break
        else:
            print("❌ Opção inválida.")

menu_principal()