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
        """Mostra dashboard com estética mais agradável (estilo estudante)."""
        # tenta limpar tela
        if self.console and hasattr(self.console, "limpar_tela"):
            try:
                self.console.limpar_tela()
            except Exception:
                pass

        # normaliza dados do usuário para um dicionário simples
        if isinstance(usuario, dict):
            dados_usuario = usuario
        else:
            try:
                dados_usuario = {
                    "usuario": getattr(usuario, "usuario", getattr(usuario, "nome", "N/A")),
                    "nivel": getattr(usuario, "nivel", "N/A"),
                    "instituicao": getattr(usuario, "instituicao", "N/A"),
                    "periodo_atual": getattr(usuario, "periodo", "N/A"),
                    "xp": getattr(usuario, "xp", 0),
                }
            except Exception:
                dados_usuario = {
                    "usuario": "N/A",
                    "nivel": "N/A",
                    "instituicao": "N/A",
                    "periodo_atual": "N/A",
                    "xp": 0,
                }

        # cabeçalho com usuário / info
        self._print(f"Usuário: {dados_usuario.get('usuario', 'N/A')}  \n--------------------------")
        self._print(
            f"Nível: {dados_usuario.get('nivel', 'N/A')} | Universidade: {dados_usuario.get('instituicao', 'N/A')} | Período: {dados_usuario.get('periodo_atual', 'N/A')}"
        )
        self._print("---------------------------------------------------")

        # barra de XP estilo blocos (dinâmica)
        try:
            xp = float(dados_usuario.get("xp", 0))
        except Exception:
            xp = 0.0
        try:
            xp_para = float(xp_para_proximo) if xp_para_proximo and float(xp_para_proximo) > 0 else 100.0
        except Exception:
            xp_para = 100.0

        pct = min(max(xp / xp_para, 0.0), 1.0)
        bar_len = 25
        cheios = int(pct * bar_len)
        vazios = bar_len - cheios
        bar_str = "■" * cheios + "□" * vazios
        self._print(f"XP: [{bar_str}]")

        self._print("--------------------------------------------------------")
        self._print("Próximas Entregas:")
        # exemplo de destaque simples (estudante)
        self._print("Implementar futuramente essa opção! [O_o]")
        self._print("--------------------------------------------------------\n")

        # mostrar opções agrupadas em duas colunas (estética)
        if not opcoes:
            self._print("Nenhuma opção disponível.")
            return

        # formata cada opção como string
        ops = [ (o[0] if isinstance(o, (list,tuple)) else str(o)) for o in opcoes ]

        # imprime duas por linha
        i = 0
        while i < len(ops):
            left_idx = i + 1
            left_txt = f"{left_idx}. {ops[i]}"
            right_txt = ""
            if i + 1 < len(ops):
                right_idx = i + 2
                right_txt = f"{right_idx}. {ops[i+1]}"
            # ajusta espaçamento (ajuste conforme largura do seu terminal)
            line = f"{left_txt.ljust(30)}{right_txt}"
            self._print(line)
            i += 2


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