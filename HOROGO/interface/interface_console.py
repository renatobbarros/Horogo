import os
import sys
import time

class InterfaceConsole:

    def __init__(self):
        # detecta Windows ou Unix simples
        self.sistema = "nt" if sys.platform == "win32" else "posix"

    def limpar_tela(self):
        """Limpa a tela (usa cls no Windows, clear nos outros)."""
        if self.sistema == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def exibir_titulo(self, titulo):
        print("\n" + "=" * 40)
        print(f"  {str(titulo)}")
        print("=" * 40 + "\n")

    def exibir_mensagem(self, mensagem, delay_segundos=None):
        print("->", mensagem)
        if delay_segundos:
            try:
                time.sleep(float(delay_segundos))
            except Exception:
                pass

    def exibir_erro(self, erro):
        """Imprime mensagem de erro simples."""
        print("ERRO:", erro)

    def exibir_sucesso(self, mensagem):
        """Imprime mensagem de sucesso simples."""
        print("SUCESSO:", mensagem)

    def exibir_lista(self, items, titulo=""):
        """Imprime uma lista numerada."""
        if titulo:
            print("\n" + titulo + ":")
        for i, item in enumerate(items, 1):
            print(f"  {i}. {item}")

    def obter_entrada(self, prompt=""):
        """Pede entrada ao usuário e retorna a string (sem espaços nas pontas)."""
        if prompt:
            return input(f"{prompt}: ").strip()
        return input().strip()

    def obter_numero(self, prompt=""):
        """Tenta ler um inteiro; repete até o usuário digitar um inteiro válido."""
        while True:
            val = self.obter_entrada(prompt)
            try:
                return int(val)
            except Exception:
                self.exibir_erro("Digite um número inteiro válido.")

    def obter_decimal(self, prompt=""):
        """Tenta ler um float; repete até ser válido."""
        while True:
            val = self.obter_entrada(prompt)
            try:
                return float(val)
            except Exception:
                self.exibir_erro("Digite um número decimal válido.")

    def obter_confirmacao(self, pergunta="Deseja continuar?"):
        """Pergunta S/N e retorna True para S, False para N."""
        while True:
            r = self.obter_entrada(pergunta + " (S/N)").upper()
            if r == "S":
                return True
            if r == "N":
                return False
            self.exibir_erro("Digite S ou N.")

    def exibir_menu(self, opcoes):
        """Mostra um menu e retorna a opção escolhida (1-based)."""
        self.exibir_lista(opcoes)
        return self.obter_numero("Escolha uma opção")

    def pausar(self):
        """Pausa até ENTER ser pressionado."""
        input("Pressione ENTER para continuar...")