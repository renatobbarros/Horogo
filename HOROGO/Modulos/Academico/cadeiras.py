import json
import time
from HOROGO.Modulos.utilitarios import limpar_terminal, carregar_conta, salvar_conta

def cadastrar_cadeira(usuario_logado):
    todas_as_contas = carregar_conta() 

    sair_loop = False
    while not sair_loop:
        limpar_terminal()
        print("HOROBOT: Vou te perguntar algumas coisas para adicionar essa disciplina.")
        time.sleep(1)
        print("HOROBOT: Nenhum nome deve ter mais de 50 caracteres.\n")
        time.sleep(1)
        nome_cadeira = input("HOROBOT: Qual é o nome da sua cadeira?\nUsuario: ")
        time.sleep(1)
        nome_professor = input("HOROBOT: Qual é o nome do professor(a) da cadeira?\nUsuario: ")
        time.sleep(1)
        
        try:
            tempo_cadeira = int(input("HOROBOT: No total, quantas horas tem essa cadeira?\nUsuario: "))
        except ValueError:
            print("HOROBOT: O tempo da cadeira deve ser um número. Tente novamente.")
            time.sleep(2)
            continue 

        if len(nome_cadeira) > 50 or len(nome_professor) > 50:
            limpar_terminal()
            print(f"HOROBOT: Nome da cadeira ({len(nome_cadeira)}) ou do professor ({len(nome_professor)}) é muito longo.")
            print("HOROBOT: Por favor, insira os dados novamente com menos de 50 caracteres.")
            time.sleep(4)
        else:
            print("\nHOROBOT: Cadeira validada com sucesso!")
            time.sleep(1)
            sair_loop = True


    nova_cadeira = {
        "nome_cadeira": nome_cadeira,
        "nome_professor": nome_professor,
        "tempo_cadeira": tempo_cadeira
    }


    if "cadeiras" not in todas_as_contas[usuario_logado]:
        todas_as_contas[usuario_logado]["cadeiras"] = []

    todas_as_contas[usuario_logado]["cadeiras"].append(nova_cadeira)

    salvar_conta(todas_as_contas)
    
    print("HOROBOT: Cadeira adicionada ao seu perfil e salva com sucesso!")
    time.sleep(2)

