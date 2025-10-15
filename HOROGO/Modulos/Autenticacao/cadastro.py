import getpass
import time
import json
import os

from HOROGO.Modulos.utilitarios import limpar_terminal, salvar_conta, carregar_conta
from HOROGO.Modulos.Autenticacao.login import sistema_login

def sistema_cadastro():
    print("HOROBOT: Certo, vamos criar sua conta no HOROGO.")
    time.sleep(1)

    while True:
        usuario_pre_lowercase = input(str("HOROBOT: Digite o nome de usuario que você deseja utilizar:\nUsuario: "))
        #o .lower vai resolver a situação em que esquecemos de colocar uma letra maiuscula ou minuscula no cadastro, isso só vai importar para a senha
        criar_usuario = usuario_pre_lowercase.lower()
        if 0 < len(criar_usuario) <= 20:
            break
        else:
            input("HOROBOT: Seu nome de usuario deve ter entre 1 e 20 caracteres. Por favor, tente novamente.")
            time.sleep(1)
            limpar_terminal()

    
    while True:
        limpar_terminal()
        criar_senha = getpass.getpass(str("HOROBOT: Muito bem, agora, crie a senha de ate 12 caracteres para sua conta:\n"))
        if 0 < len(criar_senha) <= 12:
            break
        else:
            input("HOROBOT: Sua senha deve ter entre 1 e 12 caracteres. Por favor, digite uma senha válida.")
            time.sleep(1)
            limpar_terminal()

    print("HOROBOT: Ótimo! Agora, vamos inserir seus dados acadêmicos, como sua instituição de ensino e qual período você está.")
    instituicao_pre_lowercase= input(str("HOROBOT: Insira sua instituição de ensino.\nUsuario: "))
    instituicao = instituicao_pre_lowercase.lower()
    #mudar o periodo atual por int e limitar a 15
    periodo_atual = input(str("HOROBOT: Agora, insira o período atual do seu curso.\nUsuario: "))
    print("HOROBOT: Muito bem! Sua conta agora foi criada, vou te pedir pra colocar elas novamente só pra gente conferir se está tudo ok.")
    time.sleep(1)
    limpar_terminal()

    conta_criada = carregar_conta()

    #isaque, me explica isso aqui depois por favor
    conta_criada[criar_usuario] = {
        'usuario': criar_usuario,
        'senha': criar_senha.strip(),
        'instituicao': instituicao,
        'periodo_atual': periodo_atual
    }
    
    salvar_conta(conta_criada)
    sistema_login()
        
    


        