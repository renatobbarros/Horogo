import getpass
import time
import json
import os

from HOROGO.Modulos.utilitarios import limpar_terminal, salvar_conta, carregar_conta
from HOROGO.Modulos.Autenticacao.login import sistema_login

def sistema_cadastro():
    print("HOROBOT: Certo, vamos criar sua conta no HOROGO.")
    time.sleep(1)

    # variavel criada so pra verificar se criar_usuario ja existe dentro do arquivo de conta, talvez exista uma maneira melhor de fazer isso, mas eu não sou Isaac Newton
    conta = carregar_conta()

    while True:
        usuario_pre_lowercase = input(str("HOROBOT: Digite o nome de usuario que você deseja utilizar:\nUsuario: "))
        #o .lower vai resolver a situação em que esquecemos de colocar uma letra maiuscula ou minuscula no cadastro, isso só vai importar para a senha
        criar_usuario = usuario_pre_lowercase.lower()
        if 0 < len(criar_usuario) <= 20:
            if criar_usuario in conta:
                escolha = input(f"HOROBOT: O nome de usuario '{criar_usuario}' já está em uso. Por favor, escolha outro ou entre nesta conta.")
                if escolha == 1:
                    print('HOROBOT:Certo, vamos tentar criar sua conta novamente.')
                    limpar_terminal()
                    sistema_cadastro()
                    break
                elif escolha == 2:
                    print('HOROBOT: Otimo! Irei enviar você para o nosso sistema de login.')
                    limpar_terminal()
                    sistema_login()
                    break
            else:
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

    # sistema de loop criado pra verificar se o periodo e um digito e se ele e um numero valido.
    while True:
        periodo_entrada = input("HOROBOT: Agora, insira o período atual do seu curso.\nUsuario: ")
        if periodo_entrada.isdigit() and 0 < int(periodo_entrada) <= 15:
            periodo_atual = int(periodo_entrada)
            print("HOROBOT: Muito bem! Sua conta agora foi criada, vou te pedir pra colocar elas novamente só pra gente conferir se está tudo ok.")
            break
        else:
            print("HOROBOT: Sua entrada de periodo não contem um número valido. Por favor, insira um número de periodo valido e tente novamente.")
            time.sleep(1)
            limpar_terminal()

    time.sleep(1)
    limpar_terminal()

    conta_criada = carregar_conta()

    conta_criada[criar_usuario] = {
        'usuario': criar_usuario,
        'senha': criar_senha.strip(),
        'instituicao': instituicao,
        'periodo_atual': periodo_atual,
    }

    
    salvar_conta(conta_criada)
    return criar_usuario
        
    


        