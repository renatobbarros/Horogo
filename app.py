import time
from HOROGO.Modulos.horobot import horobot_apresentacao
from HOROGO.Modulos.Autenticacao.login import sistema_login
from HOROGO.Modulos.Autenticacao.cadastro import sistema_cadastro 
from HOROGO.Modulos import variaveis_globais
from HOROGO.Modulos.utilitarios import boas_vindas_menu, limpar_terminal
from HOROGO.Modulos.Menu import menu_inicial, boas_vindas_novo_usuario
from HOROGO.Modulos.Academico.cadeiras import cadastrar_cadeira

limpar_terminal()
print(horobot_apresentacao)
time.sleep(1)
print("HOROBOT: É um prazer te receber aqui!")
time.sleep(1)
print("HOROBOT: Serei seu amigo e guia durante sua jornada academica!")
time.sleep(1)
print("HOROBOT: Antes de mais nada, você já possui cadastro no HOROGO?")
time.sleep(1)
possuicadastro = int(input("1 - Sim \n2 - Não \nUSUARIO: "))

limpar_terminal()

loop = 0
while loop == 0:
    if possuicadastro == 1:
        print("HOROBOT: Perfeito! me passe as seguintes informações para que eu te deixe onde parou da ultima vez")
        time.sleep(2)
        sistema_login()
        loop = 1
    elif possuicadastro == 2:
        sistema_cadastro()
        loop = 1
    else:
        print(f"O valor que você digitou: {possuicadastro}, não esta dentro das opçoes que te dei, por favor, digite apenas 1 ou 2 ")
        possuicadastro = int(input("1 - Sim \n2 - Não \nUSUARIO: "))


# app.py
def main():
    if variaveis_globais.logado: 

        menu_inicial(variaveis_globais.logado) 
    else:
        print("Até a proxima")

main()
