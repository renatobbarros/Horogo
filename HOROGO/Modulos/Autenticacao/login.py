import time
import getpass
import json 
from HOROGO.Modulos.utilitarios import limpar_terminal
from HOROGO.Modulos import variaveis_globais

def sistema_login():
    from HOROGO.Modulos.Autenticacao import cadastro

    limpar_terminal()

    entrada_usuario = input("HOROBOT: Digite seu nome de usuario:\nUSUARIO: ")
    time.sleep(1)
    entrada_senha = getpass.getpass("HOROBOT: Digite sua senha:\nSENHA: ")

    #isaque, aqui é a parte do json
    usuario_correto = "teste"
    senha_correta = "123"
    
    time.sleep(1)
    limpar_terminal()

    if entrada_usuario == usuario_correto and entrada_senha == senha_correta:
        print("HOROBOT: Você agora esta logado!")
        variaveis_globais.logado = "SIM"
        time.sleep(2)
    else:
        print("HOROBOT: Seu nome de usuario ou senha estão incorretos.")
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