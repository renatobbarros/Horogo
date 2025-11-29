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
        print(texto)

    def _input(self, prompt):
        if self.console and hasattr(self.console, "obter_entrada"):
            try:
                return self.console.obter_entrada(prompt)
            except Exception:
                pass
        return input(f"\n  {prompt}\n  » ").strip()

    def _xp_bar(self, xp, xp_para_proximo=100):
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
        bar = "█" * cheios + "░" * vazios
        return f"[{bar}] {int(pct*100)}%"

    def mostrar_dashboard(self, usuario, opcoes, xp_para_proximo=None, servico_xp=None):
        if self.console and hasattr(self.console, "limpar_tela"):
            try:
                self.console.limpar_tela()
            except Exception:
                pass

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

        if servico_xp:
            try:
                nome = dados_usuario.get("usuario", "N/A")
                stats = servico_xp.obter_estatisticas(nome)
                if stats:
                    dados_usuario["nivel"] = stats.get("nivel", dados_usuario.get("nivel", 1))
                    dados_usuario["titulo"] = stats.get("titulo", "")
                    xp_para_proximo = stats.get("xp_faltando", 100)
            except Exception:
                pass

        print("\n")
        print("━" * 70)
        print(f"  HOROGO".center(70))
        print("━" * 70)
        print()
        
        titulo = dados_usuario.get("titulo", "")
        if titulo:
            print(f"  👤 {dados_usuario.get('usuario', 'N/A')} - {titulo}")
        else:
            print(f"  👤 {dados_usuario.get('usuario', 'N/A')}")
        
        print(f"  🎓 {dados_usuario.get('instituicao', 'N/A')} | Período {dados_usuario.get('periodo_atual', 'N/A')}")
        print()
        
        try:
            xp = float(dados_usuario.get("xp", 0))
        except Exception:
            xp = 0.0
        
        if xp_para_proximo is None:
            xp_para_proximo = 100
        
        print(f"  ⭐ Nível {dados_usuario.get('nivel', 1)} | XP: {self._xp_bar(xp, xp + xp_para_proximo)}")
        if xp_para_proximo > 0:
            print(f"     Faltam {xp_para_proximo} XP para o próximo nível")
        else:
            print(f"     🏆 Nível Máximo Alcançado!")
        print()
        print("─" * 70)
        print()

        if not opcoes:
            self._print("  Nenhuma opção disponível.")
            return

        i = 0
        while i < len(opcoes):
            left_idx = i + 1
            left_txt = f"[{left_idx}] {opcoes[i]}"
            right_txt = ""
            
            if i + 1 < len(opcoes):
                right_idx = i + 2
                right_txt = f"[{right_idx}] {opcoes[i+1]}"
            
            print(f"  {left_txt.ljust(32)}{right_txt}")
            i += 2

        print()
        print("─" * 70)
        print()

    def selecionar_opcao(self, quantidade):
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise ValueError("quantidade deve ser inteiro > 0")
        
        while True:
            escolha = input("  » ").strip()
            try:
                n = int(escolha)
                if 1 <= n <= quantidade:
                    return n - 1
            except Exception:
                pass
            
            if self.console and hasattr(self.console, "exibir_erro"):
                try:
                    self.console.exibir_erro("Opção inválida. Digite um número válido")
                    continue
                except Exception:
                    pass
            print("  ✗ Opção inválida. Digite um número válido.")