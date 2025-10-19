import time
import getpass
import json 
from HOROGO.Modulos.utilitarios import limpar_terminal, carregar_conta
from HOROGO.Modulos import variaveis_globais

def sistema_login():
    from HOROGO.Modulos.Autenticacao import cadastro

    while True:
        limpar_terminal()
        #no meu terminal esta bugado, depois de criar uma conta, ainda aparece na parte de cima "HOROGO: Certo, vsmos crias sua conta"
        entrada_usuario = input("HOROBOT: Digite seu nome de usuario:\nUSUARIO: ")
        time.sleep(1)
        entrada_senha = getpass.getpass("HOROBOT: Digite sua senha:\nSENHA: ")

        conta = carregar_conta()

        time.sleep(1)
        limpar_terminal()

        if entrada_usuario in conta:
            
            senha_salva = conta[entrada_usuario]['senha'].strip()
            if entrada_senha.strip() == senha_salva:
                print("HOROBOT: Você agora esta logado!")
                variaveis_globais.logado = entrada_usuario
                time.sleep(2)
                break
            else:
                print("HOROBOT: Seu nome de usuario ou senha estão incorretos.")
                tratar_login_falho()
        else:
            # Se o usuário NÃO existe, avisa e trata o erro
            print('HOROBOT: Sua conta não existe no HOROGO.')
            tratar_login_falho()

def tratar_login_falho():
    from HOROGO.Modulos.Autenticacao import cadastro
    while True:
        try:
            print("\nHOROBOT: Deseja tentar novamente ou prefere criar uma conta?")
            print("1 - Tentar novamente")
            print("2 - Criar conta")
            escolha = int(input("USUARIO: "))

            if escolha == 1:
                sistema_login()  
                break
            elif escolha == 2:
                cadastro.sistema_cadastro()
                break
            else:
                print("HOROBOT: Por favor, digite apenas 1 ou 2.")
        except ValueError:
            print("HOROBOT: Por favor, digite um número válido.")