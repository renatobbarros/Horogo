import math

class InterfaceMenu:

    def __init__(self, console=None, xp_bar_width=30):
        self.console = console
        try:
            self.xp_bar_width = int(xp_bar_width)
            if self.xp_bar_width < 1:
                self.xp_bar_width = 30
        except Exception:
            self.xp_bar_width = 30

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
        """Barra simples de XP (porcentagem)."""
        try:
            xp = float(xp)
        except Exception:
            xp = 0.0
        try:
            xp_para_proximo = float(xp_para_proximo)
            if xp_para_proximo <= 0:
                xp_para_proximo = 100.0
        except Exception:
            xp_para_proximo = 100.0

        pct = min(max(xp / xp_para_proximo, 0.0), 1.0)
        cheios = int(pct * self.xp_bar_width)
        vazios = self.xp_bar_width - cheios
        bar = "=" * cheios + " " * vazios
        return f"[{bar}] {int(pct*100)}% ({int(xp)}/{int(xp_para_proximo)})"

    def mostrar_dashboard(self, usuario, opcoes, xp_para_proximo=100):
        """Mostra dashboard com nome, barra de XP e opções numeradas."""
        # tenta limpar tela
        if self.console and hasattr(self.console, "limpar_tela"):
            try:
                self.console.limpar_tela()
            except Exception:
                pass

        nome = (usuario or {}).get("nome") if isinstance(usuario, dict) else getattr(usuario, "usuario", "Usuário")
        xp = (usuario or {}).get("xp", 0) if isinstance(usuario, dict) else getattr(usuario, "xp", 0)

        # título simples
        if self.console and hasattr(self.console, "exibir_titulo"):
            try:
                self.console.exibir_titulo("Dashboard")
            except Exception:
                self._print("=== Dashboard ===")
        else:
            self._print("=== Dashboard ===")

        self._print(f"Nome: {nome}")
        self._print(f"XP : {self._xp_bar(xp, xp_para_proximo)}\n")

        # lista de opções
        if not opcoes:
            self._print("Nenhuma opção disponível.")
            return

        for i, opc in enumerate(opcoes, 1):
            if isinstance(opc, (list, tuple)):
                texto = opc[0] if len(opc) == 1 else f"{opc[0]} - {opc[1]}"
            else:
                texto = str(opc)
            self._print(f"{i}. {texto}")

    def selecionar_opcao(self, quantidade):
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise ValueError("quantidade deve ser inteiro > 0")
        while True:
            escolha = self._input("Escolha uma opção (número)")
            try:
                n = int(escolha)
                if 1 <= n <= quantidade:
                    return n - 1
            except Exception:
                pass
            if self.console and hasattr(self.console, "exibir_erro"):
                try:
                    self.console.exibir_erro("Opção inválida. Digite um número válido.")
                    continue
                except Exception:
                    pass
            self._print("Opção inválida. Digite um número válido.")