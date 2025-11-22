import os
import time
import json

class Dados:
    @staticmethod
    def salvar_conta(dados, nome_arquivo="conta.json"):
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as arq:
                json.dump(dados, arq, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"HOROBOT: Erro ao salvar o arquivo {nome_arquivo}: {e}")

    @staticmethod
    def carregar_conta(arquivo="conta.json"):
        if not (os.path.exists(arquivo) and os.path.getsize(arquivo) > 0):
            return {}
        try:
            with open(arquivo, 'r', encoding='utf-8') as arq:
                return json.load(arq)
        except json.JSONDecodeError:
            print(f"HOROBOT: O arquivo {arquivo} está corrompido. Criando um novo.")
            return {}
        except IOError as e:
            print(f"HOROBOT: Erro ao carregar o arquivo {arquivo}: {e}")
            return {}
        
class Utilitarios:
    @staticmethod
    def limpar_terminal():
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def boas_vindas_menu(nome_usuario):
        Utilitarios.limpar_terminal()
        print("HOROBOT: Bem vindo ao menu do HOROGO!")
        time.sleep(1)
        print("HOROBOT: Aqui você poderá escolher fazer o que quiser, a qualquer momento.")
        time.sleep(1)
        print(f'HOROBOT: Então, seja bem vindo, {nome_usuario}!')
        time.sleep(1)

# adicionar na parte de situação de cadeiras
    @staticmethod
    def exibir_cadeiras(usuario_logado, todas_as_contas):
        Utilitarios.limpar_terminal()
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

    @staticmethod
    def pagina_em_construcao():
        Utilitarios.limpar_terminal()
        print("DEVS: Parabéns! Você acabou de acessar uma parte em desenvolvimento.")
        print("DEVS: Mas a sua pagina desejada esta em outro castelo...")
        print("DEVS: Esta funcionalidade será implementada em breve! O7")
        print("DEVS: Voltando ao menu em 3 segundos...")
        time.sleep(3)
        Utilitarios.limpar_terminal()

    @staticmethod
    def exibir_mensagem_espera(mensagem, segundos=1):
        print(mensagem)
        time.sleep(segundos)