import os
import time
import json

def limpar_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def boas_vindas_menu():
    print("HOROBOT: Bem vindo ao menu do HOROGO!")
    time.sleep(1)
    print("HOROBOT: Aqui você poderá escolher fazer o que quiser, a qualquer momento.")

def achar_proximo_id(lista):

    if not lista:
        return 1
    return lista[-1]['id'] + 1
