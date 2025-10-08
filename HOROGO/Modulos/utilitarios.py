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



def carregar_dados(): # Eu coloquei esse codigo do repo de lucas so pra eu entender como que funciona, mais ou menos. Não vai ficar assim, não.. eu acho.
    if not os.path.exists('conta.json'): # Em caso de não existir o arquivo, retorna um dicionário vazio
        return {}
    with open('conta.json', 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)
    return dados