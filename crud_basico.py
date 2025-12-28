''' 
SISTEMA CRUD EM PYTHON

Funcionalidades:
   - Cadastro de usuários
   - Login com senha criptografada
   - Persistência em arquivo JSON
   - Operações CRUD básicas 

'''
#─────────────────────────────────────────────────────────────────────────────────
# IMPORTAÇÕES

import json         # - Persistência de dados em arquivo JSON
import os           # - Verificação de existência de arquivo
import re           # - Validação de email
import hashlib      # - Criptografia de senha (hash)

ARQUIVO = 'usuarios.json' 

#─────────────────────────────────────────────────────────────────────────────────
#  FUNÇÕES UTILITÁRIAS
#─────────────────────────────────────────────────────────────────────────────────

def carregar_dados():  
    '''
    Carrega os usuários do arquivo JSON.
    Retorna uma lista vazia caso o arquivo não exista.
    '''
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_dados(dados):  
    '''
    Salva a lista de usuários no arquivo JSON.
    '''
    with open(ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4)

def hash_senha(senha):  
    '''
    Gera o hash da senha para armazenamento seguro.
    '''  
    return hashlib.sha256(senha.encode()).hexdigest()

def email_valido(email):  
    '''
    Valida se o email está em um formato básico aceitável.
    '''
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email)

#─────────────────────────────────────────────────────────────────────────────────
# CLASSES 
#─────────────────────────────────────────────────────────────────────────────────
class Usuario: 
    '''
    Representa um usuário do sistema.
    '''
    def __init__(self, id, nome, email, senha_hash):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash

    def to_dict(self): 
        '''
        Converte o objeto Usuario para dicionário,
        permitindo persistência em JSON.
        '''
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'senha': self.senha_hash
        }

class UsuarioCRUD: 
    '''
    Classe responsável pelas operações CRUD
    e autenticação de usuários.
    '''
    def __init__(self):
        self.usuarios = carregar_dados()
        self.proximo_id = self._gerar_proximo_id()

    def _gerar_proximo_id(self):
        '''
        Gera o próximo ID disponível de forma sequencial.
        '''
        if not self.usuarios:
            return 1
        return max(u['id'] for u in self.usuarios) + 1

    def cadastrar(self):
        '''
        Realiza o cadastro de um novo usuário
        aplicando validações básicas.
        '''
        nome = input('Nome: ')
        email = input('Email: ')

        if not email_valido(email):
            print('Email inválido.')
            return

        # Evita cadastro duplicado por Email
        if any(u['email'] == email for u in self.usuarios):
            print('Email já cadastrado.')
            return

        senha = input('Senha: ')
        senha_hash = hash_senha(senha)

        usuario = Usuario(self.proximo_id, nome, email, senha_hash)
        self.usuarios.append(usuario.to_dict())
        salvar_dados(self.usuarios)

        self.proximo_id += 1
        print('Usuário cadastrado com sucesso!')

    def listar(self):
        '''
         Lista todos os usuários cadastrados.
        '''
        if not self.usuarios:
            print('Nenhum usuário cadastrado.')
            return

        for u in self.usuarios:
            print(f'ID: {u['id']} | Nome: {u['nome']} | Email: {u['email']}')

    def atualizar(self):
        '''
        Atualiza os dados de um usuário existente.
        '''
        id_busca = int(input('ID do usuário: '))

        for u in self.usuarios:
            if u['id'] == id_busca:
                u['nome'] = input('Novo nome: ')
                salvar_dados(self.usuarios)
                print('Usuário atualizado.')
                return

        print('Usuário não encontrado.')

    def deletar(self):
        '''
        Remove um usuário do sistema.
        '''
        id_busca = int(input('ID do usuário: '))

        for u in self.usuarios:
            if u['id'] == id_busca:
                self.usuarios.remove(u)
                salvar_dados(self.usuarios)
                print('Usuário removido.')
                return

        print('Usuário não encontrado.')

    def login(self):
        '''
        Realiza a autenticação do usuário.
        '''
        email = input('Email: ')
        senha = input('Senha: ')
        senha_hash = hash_senha(senha)

        for u in self.usuarios:
            if u['email'] == email and u['senha'] == senha_hash:
                print(f'\nLogin realizado! Bem-vinda, {u['nome']}')
                return True

        print('Email ou senha inválidos.')
        return False
    
#─────────────────────────────────────────────────────────────────────────────────
# MENUS 
#─────────────────────────────────────────────────────────────────────────────────
def menu_principal():
    '''
    Menu inicial do sistema.
    '''
    crud = UsuarioCRUD()

    while True:
        print('\n── SISTEMA ── .✦')
        print('┆ 1 - Cadastrar')
        print('┆ 2 - Login')
        print('┆ 0 - Sair')

        opcao = input('Escolha: ')

        if opcao == '1':
            crud.cadastrar()
        elif opcao == '2':
            if crud.login():
                menu_usuario(crud)
        elif opcao == '0':
            print('Saindo...')
            break
        else:
            print('✖ Opção inválida.')

def menu_usuario(crud):
    '''
    Menu disponível após login.
    '''
    while True:
        print('\n── MENU USUÁRIO ── .✦')
        print('┆ 1 - Listar usuários')
        print('┆ 2 - Atualizar usuário')
        print('┆ 3 - Deletar usuário')
        print('┆ 0 - Logout')

        opcao = input('Escolha: ')

        if opcao == '1':
            crud.listar()
        elif opcao == '2':
            crud.atualizar()
        elif opcao == '3':
            crud.deletar()
        elif opcao == '0':
            print('✔ Logout realizado.')
            break
        else:
            print('✖ Opção inválida.')

menu_principal()