import os
import sys
import time

class InterfaceConsole:
    def __init__(self):
        self.sistema = "nt" if sys.platform == "win32" else "posix"

    def limpar_tela(self):
        if self.sistema == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def exibir_titulo(self, titulo):
        print("\n")
        print("━" * 60)
        print(f"  {str(titulo).upper()}")
        print("━" * 60)
        print()

    def exibir_secao(self, titulo):
        print(f"\n▸ {titulo}")
        print("─" * 50)

    def exibir_mensagem(self, mensagem, delay_segundos=None, typing_speed=None):
        if typing_speed is not None:
            try:
                self.digitar(str(mensagem), velocidade=typing_speed)
            except Exception:
                print(f"  {mensagem}")
        else:
            print(f"  {mensagem}")

        if delay_segundos:
            try:
                time.sleep(float(delay_segundos))
            except Exception:
                pass

    def digitar(self, mensagem: str, velocidade: float = 0.02):
        try:
            if not velocidade or float(velocidade) <= 0:
                sys.stdout.write("  " + str(mensagem) + "\n")
                sys.stdout.flush()
                return

            sys.stdout.write("  ")
            for ch in str(mensagem):
                sys.stdout.write(ch)
                sys.stdout.flush()
                time.sleep(float(velocidade))
            sys.stdout.write("\n")
            sys.stdout.flush()
        except Exception:
            print(f"  {mensagem}")

    def exibir_erro(self, erro):
        print(f"\n  ✗ {erro}")

    def exibir_sucesso(self, mensagem):
        print(f"\n  ✓ {mensagem}")

    def exibir_aviso(self, mensagem):
        print(f"\n  ⚠ {mensagem}")

    def exibir_lista(self, items, titulo=""):
        if titulo:
            print(f"\n{titulo}:")
            print()
        for i, item in enumerate(items, 1):
            print(f"  [{i}] {item}")

    def exibir_opcoes(self, opcoes, titulo=""):
        if titulo:
            self.exibir_secao(titulo)
        print()
        for i, opcao in enumerate(opcoes, 1):
            print(f"  [{i}] {opcao}")
        print()

    def obter_entrada(self, prompt=""):
        if prompt:
            return input(f"\n  {prompt}\n  » ").strip()
        return input("  » ").strip()

    def obter_numero(self, prompt=""):
        while True:
            val = self.obter_entrada(prompt)
            try:
                return int(val)
            except Exception:
                self.exibir_erro("Digite um número inteiro válido")

    def obter_decimal(self, prompt=""):
        while True:
            val = self.obter_entrada(prompt)
            try:
                return float(val)
            except Exception:
                self.exibir_erro("Digite um número decimal válido")

    def obter_confirmacao(self, pergunta="Deseja continuar?"):
        while True:
            r = input(f"\n  {pergunta} [S/N]\n  » ").strip().upper()
            if r == "S":
                return True
            if r == "N":
                return False
            self.exibir_erro("Digite S ou N")

    def exibir_menu(self, opcoes):
        self.exibir_opcoes(opcoes)
        return self.obter_numero("Escolha uma opção")

    def pausar(self):
        input("\n  Pressione ENTER para continuar...")

    def separador(self):
        print("\n" + "─" * 60 + "\n")