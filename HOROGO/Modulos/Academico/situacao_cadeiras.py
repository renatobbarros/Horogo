import json
import time
from HOROGO.Modulos.utilitarios import limpar_terminal, carregar_conta, salvar_conta
from HOROGO.Modulos.Academico.cadastro_notas import cadastrar_cadeira

def situacao_cadeiras(usuario_logado):
    conta = carregar_conta()

    dados_importantes = conta.get(usuario_logado)

    # se existir cadeira, ele continua. caso não exista, ou não tem nada dentro da cadeira, ele manda cadastrar.
    if "cadeiras" not in dados_importantes or not dados_importantes["cadeiras"]:
        print("HOROBOT: Você não tem nenhuma cadeira cadastrada.")
        time.sleep(2)
        cadastrar_cadeira()
        return

    print("HOROBOT: Aqui está a situação de suas cadeiras.\n")
    
    for i, cadeira in enumerate(dados_importantes["cadeiras"]):
        print(f'----------------- CADEIRA {i+1} ------------------')
        print(f"Nome da Cadeira: {cadeira.get('nome_cadeira', 'N/A')}")
        print(f"Professor(a):   {cadeira.get('nome_professor', 'N/A')}")
        print(f"Tempo Total:    {cadeira.get('tempo_cadeira', 'N/A')} horas")
        print('----------------------------------------------------')
     
    limpar_terminal()



