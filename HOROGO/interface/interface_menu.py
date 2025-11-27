import math

class InterfaceMenu:
    def __init__(self, console=None, xp_bar_width=30):
        """
        console: instância de InterfaceConsole (opcional)
        xp_bar_width: largura do indicador de XP
        """
        self.console = console
        self.xp_bar_width = xp_bar_width

    def _print(self, texto):
        if self.console and hasattr(self.console, "exibir_mensagem"):
            try:
                self.console.exibir_mensagem(texto)
                return
            except Exception:
                pass
        print(texto)

    def _input(self, prompt):
        if self.console and hasattr(self.console, "obter_entrada"):
            try:
                return self.console.obter_entrada(prompt)
            except Exception:
                pass
        return input(f"{prompt}: ").strip()

    def _xp_bar(self, xp, xp_para_proximo=100):
        """Retorna string com barra visual de XP"""
        pct = min(max(xp / xp_para_proximo, 0.0), 1.0)
        cheios = math.floor(pct * self.xp_bar_width)
        vazios = self.xp_bar_width - cheios
        return f"[{'█' * cheios}{' ' * vazios}] {int(pct*100)}% ({xp}/{xp_para_proximo})"

    def mostrar_dashboard(self, usuario, opcoes, xp_para_proximo=100):
        """
        Exibe dashboard com nome, XP e lista de opções.
        usuario: dict com ao menos 'nome' e 'xp' (ex: {'nome':'Renat','xp':42})
        opcoes: lista de strings ou tuplas (texto, descricao)
        """
        # limpar tela se possível
        if self.console and hasattr(self.console, "limpar_tela"):
            try:
                self.console.limpar_tela()
            except Exception:
                pass

        nome = usuario.get("nome", "Usuário")
        xp = usuario.get("xp", 0)

        # título
        if self.console and hasattr(self.console, "exibir_titulo"):
            try:
                self.console.exibir_titulo("Dashboard")
            except Exception:
                self._print("=== Dashboard ===")
        else:
            self._print("=== Dashboard ===")

        # cabeçalho com nome e XP
        self._print(f"Nome: {nome}")
        self._print(f"XP : {self._xp_bar(xp, xp_para_proximo)}\n")

        # opções numeradas
        linhas = []
        for i, op in enumerate(opcoes, 1):
            if isinstance(op, (list, tuple)):
                texto = f"{op[0]} - {op[1]}" if len(op) > 1 else op[0]
            else:
                texto = str(op)
            linhas.append(f"{i}. {texto}")
        if linhas:
            for linha in linhas:
                self._print(linha)
        else:
            self._print("Nenhuma opção disponível.")

    def selecionar_opcao(self, quantidade):
        """Solicita seleção numérica (1..quantidade) e retorna índice (0-based)"""
        while True:
            escolha = self._input("Escolha uma opção (número)")
            try:
                n = int(escolha)
                if 1 <= n <= quantidade:
                    return n - 1
            except ValueError:
                pass
            # mensagem de erro via console se disponível
            if self.console and hasattr(self.console, "exibir_erro"):
                try:
                    self.console.exibir_erro("Opção inválida. Digite um número válido.")
                    continue
                except Exception:
                    pass
            self._print("Opção inválida. Digite um número válido.")