import time
import getpass

from HOROGO.Modulos.utilitarios import limpar_terminal
from HOROGO.Modulos import variaveis_globais

def sistema_login():
    from HOROGO.Modulos.Autenticacao import cadastro

    limpar_terminal()

    entrada_usuario = input(str("HOROBOT: Digite seu nome de usuario:\n"))
    time.sleep(1)

    entrada_senha = getpass.getpass(str("HOROBOT: Digite sua senha:\n"))
    time.sleep(1)
    limpar_terminal()

    def validacaologin():
        if variaveis_globais.usuario == entrada_usuario and variaveis_globais.senha == entrada_senha:
            print("HOROBOT: Você agora esta logado!")
            variaveis_globais.logado = "SIM"
        else:
            print("HOROBOT: Seu nome de usuario ou senha estão incorretos.")
            
            while True:
                try:
                    print("HOROBOT: Deseja tentar novamente ou prefere criar uma conta? \n1 - tentar novamente\n2 - Criar conta")
                    escolhanovamente = int(input("USUARIO: "))
                    if escolhanovamente == 1:
                        sistema_login()
                        break
                    elif escolhanovamente == 2:
                        cadastro.sistema_cadastro()
                        break
                    else:
                        print("HOROBOT: Por favor, digite apenas 1 ou 2")
                except ValueError:
                    print("HOROBOT: Por favor, digite um número válido.")

    validacaologin()