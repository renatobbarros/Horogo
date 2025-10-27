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
    print('HOROBOT: Então, seja bem vindo, {usuario}!')

def salvar_conta(dados, nome_arquivo="conta.json"):
        """Salva os dados de cadeiras em um arquivo JSON... ou pelo menos, e pra funcionar assim. T_T"""
        #o primeiro serve para selecionar o tipo de dados, o segundo para direcionar os dados para um arquivo em especifico
        with open(nome_arquivo, 'w', encoding='utf-8') as arq:
            json.dump(dados, arq, ensure_ascii=False, indent=4)
            #dump serve para exportar para o arquivo como dicionario, o dumps serviria para exportar como arquivo

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
    
def exibir_cadeiras(usuario_logado, todas_as_contas):
    """Exibe as cadeiras do usuário logado e retorna a lista de cadeiras."""
    limpar_terminal()
    print("HOROBOT: Suas cadeiras cadastradas:\n")
    
    cadeiras = todas_as_contas.get(usuario_logado, {}).get("cadeiras", [])
    
    if not cadeiras:
        print("HOROBOT: Você não tem nenhuma cadeira cadastrada.")
        time.sleep(2)
        return []

    for i, cadeira in enumerate(cadeiras):
        print(f"[{i + 1}] {cadeira['nome_cadeira']} - Professor(a): {cadeira['nome_professor']}")
    
    print("-" * 30)
    return cadeiras


def pagina_em_construcao():
    limpar_terminal()
    print("DEVS: Parabéns! Você acabou de acessar uma parte em desenvolvimento.")
    print("DEVS: Mas a sua pagina desejada esta em outro castelo...")
    print("DEVS: Esta funcionalidade será implementada em breve! O7")
    print("DEVS: Voltando ao menu em 3 segundos...")
    time.sleep(3)
