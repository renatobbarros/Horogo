import os
import time
import json

def limpar_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def boas_vindas_menu():
    print("HOROBOT: Bem vindo ao menu do HOROGO!")
    time.sleep(1)
    print("HOROBOT: Aqui você poderá escolher fazer o que quiser, a qualquer momento.")
    time.sleep(1)
    print('HOROBOT: Então, seja bem vindo, [usuario]!')

def salvar_conta(dados, nome_arquivo="conta.json"):
        """Salva os dados de cadeiras em um arquivo JSON... ou pelo menos, e pra funcionar assim. T_T"""
        with open(nome_arquivo, 'w', encoding='utf-8') as arq:
            json.dump(dados, arq, ensure_ascii=False, indent=4)

def carregar_conta(arquivo="conta.json"):
    """ Carrega dados de um arquivo JSON. Se o arquivo não existir ou estiver vazio, retorna um dicionário vazio para evitar erros."""
    
    if os.path.exists(arquivo) and os.path.getsize(arquivo) > 0:
        # Verifica se o arquivo existe, e se ele contem algo dentro. Gemini passou essa dica, decidi deixar por enquanto.
        with open(arquivo, 'r', encoding='utf-8') as arq:
            try:
                # tentar carregar o JSON, exceto se estiver corrompido ou mal formatado, nesse caso, retornar um dicionario vazio.
                return json.load(arq)
            except json.JSONDecodeError:
                print(f"Aviso: O arquivo {arquivo} está corrompido. Criando um novo.")
                return {}
    else:
        return {}


def achar_proximo_id(lista):

    if not lista:
        return 1
    return lista[-1]['id'] + 1
