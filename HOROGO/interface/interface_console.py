import os
import sys

class InterfaceConsole:
    def __init__(self):
        self.sistema = "nt" if sys.platform == "win32" else "posix"
    
    def limpar_tela(self):
        '''Limpa a tela do console'''
        comando = "cls" if self.sistema == "nt" else "clear"
        os.system(comando)
    
    def exibir_titulo(self, titulo):
        '''Exibe um título formatado'''
        print("\n" + "="*50)
        print(f"  {titulo.center(46)}")
        print("="*50 + "\n")
    
    def exibir_mensagem(self, mensagem):
        '''Exibe uma mensagem simples'''
        print(f"→ {mensagem}")
    
    def exibir_erro(self, erro):
        '''Exibe uma mensagem de erro'''
        print(f"✗ ERRO: {erro}")
    
    def exibir_sucesso(self, mensagem):
        '''Exibe uma mensagem de sucesso'''
        print(f"✓ SUCESSO: {mensagem}")
    
    def exibir_lista(self, items, titulo=""):
        '''Exibe uma lista formatada'''
        if titulo:
            print(f"\n{titulo}:")
        for i, item in enumerate(items, 1):
            print(f"  {i}. {item}")
    
    def obter_entrada(self, prompt=""):
        '''Obtém entrada do usuário'''
        return input(f"→ {prompt}: ").strip()
    
    def obter_numero(self, prompt=""):
        '''Obtém um número inteiro do usuário com validação'''
        while True:
            try:
                valor = input(f"→ {prompt}: ").strip()
                return int(valor)
            except ValueError:
                self.exibir_erro("Por favor, digite um número válido")
    
    def obter_decimal(self, prompt=""):
        '''Obtém um número decimal do usuário com validação'''
        while True:
            try:
                valor = input(f"→ {prompt}: ").strip()
                return float(valor)
            except ValueError:
                self.exibir_erro("Por favor, digite um número válido")
    
    def obter_confirmacao(self, pergunta="Deseja continuar?"):
        '''Obtém confirmação do usuário (S/N)'''
        while True:
            resposta = input(f"→ {pergunta} (S/N): ").strip().upper()
            if resposta in ['S', 'N']:
                return resposta == 'S'
            self.exibir_erro("Digite apenas 'S' ou 'N'")
    
    def exibir_menu(self, opcoes):
        '''Exibe um menu e retorna a opção selecionada'''
        self.exibir_lista(opcoes)
        while True:
            try:
                escolha = self.obter_numero("Escolha uma opção")
                if 1 <= escolha <= len(opcoes):
                    return escolha
                self.exibir_erro(f"Digite um número entre 1 e {len(opcoes)}")
            except ValueError:
                self.exibir_erro("Entrada inválida")
    
    def pausar(self):
        '''Pausa a execução até o usuário pressionar Enter'''
        input("\n→ Pressione ENTER para continuar...")   