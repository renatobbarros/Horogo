import time
import getpass
import json 


from HOROGO.Modulos.utilitarios import limpar_terminal
from HOROGO.Modulos import variaveis_globais

def sistema_login():
    from HOROGO.Modulos.Autenticacao import cadastro

    limpar_terminal()
    limpar_terminal()

    entrada_usuario = input(str("HOROBOT: Digite seu nome de usuario:\n"))
    time.sleep(1)

    entrada_senha = getpass.getpass(str("HOROBOT: Digite sua senha:\n"))

    with open( 'conta.json' , 'r' , encoding='utf-8') as arq:
        dados_conta = json.load(arq)

        nome = dados_conta["Usuario"]
        senha = dados_conta["Senha"]
    
    nome_logado = nome
    senha_logada = senha
    
    time.sleep(1)
    limpar_terminal()

    def validacaologin():
        if nome == entrada_usuario and senha == entrada_senha:
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