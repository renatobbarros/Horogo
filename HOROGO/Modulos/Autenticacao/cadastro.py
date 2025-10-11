import getpass
import time
import json
import os

from HOROGO.Modulos.utilitarios import limpar_terminal
from HOROGO.Modulos.Autenticacao.login import sistema_login


def sistema_cadastro():
    limpar_terminal()
    print("HOROBOT: Certo, vamos criar sua conta no HOROGO.")

    time.sleep(1)

    criar_usuario = input(str("HOROBOT: Digite o nome de usuario que você deseja utilizar:\nUsuario:"))

    loop_usuario = 0

    # Depois, vamo tentar fazer tudo em um loop so, se for possivel.
    while loop_usuario == 0:
        if len(criar_usuario) == 0 or len(criar_usuario) > 20:
            criar_usuario = input(str("HOROBOT: Seu nome de usuario contem mais do que 20 caracteres ou você colocou um nome vazio. Por favor, tente novamente.\n"))
        else: 
            criar_senha = getpass.getpass(str("HOROBOT: Muito bem, agora, crie a senha de ate 12 caracteres para sua conta:\n"))
            loop_usuario = 1
            usuario = str(criar_usuario)
            time.sleep(1) 
    loop_senha = 0

    while loop_senha == 0:
        if len(criar_senha) > 12:
            criar_senha = getpass.getpass(str("HOROBOT: Sua senha contem muitos caracteres. Por favor, digite uma senha mais curta:\n"))
        elif len(criar_senha) == 0:
            criar_senha = getpass.getpass(str("HOROBOT: Você não preencheu sua senha, para sua segurança, digite uma senha:\n"))
        else:
            senha = str(criar_senha)
            print(senha) #Oxe? pq a senha ta aparecendo?
            print("HOROBOT: Otimo! Agora, vamos inserir seus dados academicos, como sua instituição de ensino e qual periodo você esta.")
            instituição = input(str("HOROBOT: Insira sua instituição de ensino.\n")) #Definir instituição e nome em lower Case, colocar isso na planilha tambem
            periodo_atual = input(str("HOROBOT; Agora, insira o periodo atual do seu curso.\n"))
            print("HOROBOT: Muito bem! Sua conta agora foi criada, vou te pedir pra colocar elas novamente só pra gente conferir se esta tudo ok.")
            time.sleep(1)
            loop_senha = 1

            sistema_login()

