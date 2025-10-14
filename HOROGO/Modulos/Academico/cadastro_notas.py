import time
from HOROGO.Modulos.utilitarios import limpar_terminal, achar_proximmo_id
import json

nome = input('nome:')
senha = input('senha: ')
with open('conta.json', 'r', encoding='utf-8') as arquivo:
    dados = json.load(arquivo)
'''
with open('conta.json', 'w', encoding='utf-8') as arquivo:
    json.dump(dados, arquivo, indent=4, ensure_ascii=False)
'''
dados[nome] = {'nome': nome, 'senha': senha}

with open('conta.json', 'w', encoding='utf-8') as arquivo:
    json.dump(dados, arquivo, indent=4, ensure_ascii=False)