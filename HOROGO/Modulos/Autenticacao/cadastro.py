import getpass
import time
import json
import os

from HOROGO.Modulos.utilitarios import limpar_terminal, salvar_conta, carregar_conta
from HOROGO.Modulos.Autenticacao.login import sistema_login



def sistema_cadastro():

    

    limpar_terminal()
    print("HOROBOT: Certo, vamos criar sua conta no HOROGO.")

    time.sleep(1)

    criar_usuario = input(str("HOROBOT: Digite o nome de usuario que você deseja utilizar:\nUsuario:"))



import getpass
import time
import json
import os

from HOROGO.Modulos.utilitarios import limpar_terminal, salvar_conta, carregar_conta
from HOROGO.Modulos.Autenticacao.login import sistema_login

def sistema_cadastro():
    """Como o proprio nome diz, e o sistema de cadastro de usuario. Aqui inclui a criação do nome, senha, instituição e o periodo atual na data de criação."""
    limpar_terminal()
    print("HOROBOT: Certo, vamos criar sua conta no HOROGO.")
    time.sleep(1)

    while True:
        criar_usuario = input(str("HOROBOT: Digite o nome de usuario que você deseja utilizar:\nUsuario:"))
        if 0 < len(criar_usuario) <= 20:
            break
        else:
            input("HOROBOT: Seu nome de usuario deve ter entre 1 e 20 caracteres. Por favor, tente novamente.")
            time.sleep(1)
            limpar_terminal()

    
    while True:
        criar_senha = getpass.getpass(str("HOROBOT: Muito bem, agora, crie a senha de ate 12 caracteres para sua conta:\n"))
        if 0 < len(criar_senha) <= 12:
            break
        else:
            input("HOROBOT: Sua senha deve ter entre 1 e 12 caracteres. Por favor, digite uma senha válida.")
            time.sleep(1)
            limpar_terminal()

    print("HOROBOT: Ótimo! Agora, vamos inserir seus dados acadêmicos, como sua instituição de ensino e qual período você está.")
    instituicao = input(str("HOROBOT: Insira sua instituição de ensino.\n"))
    periodo_atual = input(str("HOROBOT: Agora, insira o período atual do seu curso.\n"))
    print("HOROBOT: Muito bem! Sua conta agora foi criada, vou te pedir pra colocar elas novamente só pra gente conferir se está tudo ok.")
    time.sleep(1)

    conta_criada = carregar_conta()

    conta_criada[criar_usuario] = {
        'usuario': criar_usuario,
        'senha': criar_senha.strip(),
        'instituicao': instituicao,
        'periodo_atual': periodo_atual
    }
    
    salvar_conta(conta_criada)
    sistema_login()
        
    


        