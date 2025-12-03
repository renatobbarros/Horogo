from math import ceil
from typing import Iterable, Any, Optional


class InterfaceAcademica:
    """Interface acadêmica com design limpo."""

    def __init__(self, console=None, servico_academico=None, col_width: int = 40):
        self.console = console
        self.servico = servico_academico
        self.col_width = int(col_width) if col_width and int(col_width) > 0 else 40

    def _print(self, texto: str):
        """Imprime via console."""
        print(f"  {texto}")

    def _input(self, prompt: str) -> str:
        if self.console and hasattr(self.console, "obter_entrada"):
            try:
                return self.console.obter_entrada(prompt)
            except Exception:
                pass
        return input(f"\n  {prompt}\n  » ").strip()

    def _repr_item(self, item) -> str:
        """Representa um item de cadeira como texto legível."""
        if isinstance(item, dict):
            nome = item.get("nome_cadeira") or item.get("nome") or "Sem nome"
            codigo = item.get("codigo") or item.get("codigo_cadeira")
            if codigo:
                return f"{nome} ({codigo})"
            return nome
        if hasattr(item, "nome_cadeira"):
            nome = getattr(item, "nome_cadeira", "Sem nome")
            codigo = getattr(item, "codigo", None) or getattr(item, "codigo_cadeira", None)
            if codigo:
                return f"{nome} ({codigo})"
            return nome
        return str(item)

    def listar_cadeiras_duas_colunas(self, cadeiras: Iterable):
        """Mostra cadeiras em duas colunas limpas."""
        if not cadeiras:
            self._print("Nenhuma cadeira encontrada.")
            return

        try:
            cadeiras = list(cadeiras)
        except Exception:
            self._print("Formato inválido de cadeiras.")
            return

        n = len(cadeiras)
        if n == 0:
            self._print("Nenhuma cadeira encontrada.")
            return

        if self.console and hasattr(self.console, "exibir_secao"):
            try:
                self.console.exibir_secao("Cadeiras Cadastradas")
            except Exception:
                print("\n▸ Cadeiras Cadastradas")
                print("─" * 60)
        else:
            print("\n▸ Cadeiras Cadastradas")
            print("─" * 60)

        rows = ceil(n / 2)
        esquerda = [self._repr_item(x) for x in cadeiras[:rows]]
        direita = [self._repr_item(x) for x in cadeiras[rows:]]
        
        while len(direita) < rows:
            direita.append("")

        for l, r in zip(esquerda, direita):
            if len(l) > self.col_width:
                l = l[: max(1, self.col_width - 3)] + "..."
            line = f"  {l.ljust(self.col_width)}  {r}"
            print(line)
        
        print()

    def executar_menu_cadastrar_cadeira(self, usuario: Any) -> bool:
        """Menu para cadastrar nova cadeira."""
        if not self.servico:
            self._print("Serviço acadêmico não configurado.")
            return False

        if self.console and hasattr(self.console, "exibir_titulo"):
            self.console.exibir_titulo("Cadastrar Cadeira")
        else:
            print("\n" + "━" * 60)
            print("  CADASTRAR CADEIRA")
            print("━" * 60 + "\n")

        self._print("📝 Preencha os dados da cadeira:")
        print()

        nome = self._input("Nome da cadeira")
        codigo = self._input("Código da cadeira")
        periodo = self._input("Período")

        if isinstance(usuario, dict):
            nome_usuario = usuario.get("usuario") or usuario.get("nome")
        else:
            nome_usuario = getattr(usuario, "usuario", getattr(usuario, "nome", None))

        if not nome_usuario:
            if self.console and hasattr(self.console, "exibir_erro"):
                self.console.exibir_erro("Não foi possível identificar o usuário")
            else:
                print("\n  ✗ Erro: não foi possível identificar o usuário")
            return False

        try:
            nova_cadeira = self.servico.criar_nova_cadeira(nome, codigo, periodo)
            ok = self.servico.adicionar_cadeira_ao_usuario(nome_usuario, nova_cadeira)
            
            if ok:
                if self.console and hasattr(self.console, "exibir_sucesso"):
                    self.console.exibir_sucesso("Cadeira cadastrada com sucesso!")
                else:
                    print("\n  ✓ Cadeira cadastrada com sucesso!")
                return True
            else:
                if self.console and hasattr(self.console, "exibir_erro"):
                    self.console.exibir_erro("Falha ao cadastrar cadeira")
                else:
                    print("\n  ✗ Falha ao cadastrar cadeira")
                return False
        except Exception as e:
            if self.console and hasattr(self.console, "exibir_erro"):
                self.console.exibir_erro(f"Erro ao cadastrar: {e}")
            else:
                print(f"\n  ✗ Erro ao cadastrar: {e}")
            return False

    def executar_situacao_cadeiras(self, usuario: Any):
        """Exibe a situação de todas as cadeiras com notas."""
        if self.console and hasattr(self.console, "exibir_titulo"):
            self.console.exibir_titulo("Situação das Cadeiras")
        else:
            print("\n" + "━" * 60)
            print("  SITUAÇÃO DAS CADEIRAS")
            print("━" * 60 + "\n")

        if hasattr(usuario, "obter_cadeiras"):
            cadeiras = usuario.obter_cadeiras()
        elif isinstance(usuario, dict):
            cadeiras = usuario.get("cadeiras", [])
        else:
            cadeiras = []

        if not cadeiras:
            self._print("Nenhuma cadeira cadastrada.")
            return

        for i, cadeira in enumerate(cadeiras, 1):
            if isinstance(cadeira, dict):
                nome = cadeira.get("nome_cadeira") or cadeira.get("nome") or "Sem nome"
                notas_dict = cadeira.get("notas")
                
                print(f"\n  [{i}] {nome}")
                print("  " + "─" * 50)
                
                if notas_dict:
                    va1 = notas_dict.get("va1", "N/A")
                    va2 = notas_dict.get("va2", "N/A")
                    va3 = notas_dict.get("va3", "N/A")
                    recuperacao = notas_dict.get("recuperacao", "N/A")
                    media_parcial = notas_dict.get("media_parcial", "N/A")
                    media_final = notas_dict.get("media_final", "N/A")
                    situacao = notas_dict.get("situacao", "N/A")
                    
                    print(f"      VA1: {va1}")
                    print(f"      VA2: {va2}")
                    print(f"      VA3: {va3}")
                    if recuperacao != "N/A" and recuperacao is not None:
                        print(f"      Recuperação: {recuperacao}")
                    print(f"      Média Parcial: {media_parcial}")
                    print(f"      Média Final: {media_final}")
                    
                    # emoji conforme situação
                    if situacao == "Aprovado":
                        print(f"      ✓ Situação: {situacao}")
                    else:
                        print(f"      ✗ Situação: {situacao}")
                else:
                    print("      Sem notas cadastradas")
            
            elif hasattr(cadeira, "nome_cadeira"):
                nome = getattr(cadeira, "nome_cadeira", "Sem nome")
                print(f"\n  [{i}] {nome}")
                print("  " + "─" * 50)
                
                if hasattr(cadeira, "notas") and cadeira.notas:
                    notas = cadeira.notas
                    print(f"      VA1: {getattr(notas, 'va1', 'N/A')}")
                    print(f"      VA2: {getattr(notas, 'va2', 'N/A')}")
                    print(f"      VA3: {getattr(notas, 'va3', 'N/A')}")
                    if hasattr(notas, 'recuperacao') and notas.recuperacao is not None:
                        print(f"      Recuperação: {notas.recuperacao}")
                    
                    if hasattr(notas, 'calcular_media_parcial'):
                        print(f"      Média Parcial: {notas.calcular_media_parcial():.2f}")
                    if hasattr(notas, 'calcular_media_final'):
                        print(f"      Média Final: {notas.calcular_media_final():.2f}")
                    if hasattr(notas, 'get_situacao'):
                        situacao = notas.get_situacao()
                        if situacao == "Aprovado":
                            print(f"      ✓ Situação: {situacao}")
                        else:
                            print(f"      ✗ Situação: {situacao}")
                else:
                    print("      Sem notas cadastradas")
        
        print()

    def executar_menu_cadastrar_notas(self, usuario: Any):
        """Menu para cadastrar/atualizar notas de uma cadeira."""
        if not self.servico:
            self._print("Serviço acadêmico não configurado.")
            return

        if self.console and hasattr(self.console, "exibir_titulo"):
            self.console.exibir_titulo("Cadastrar/Atualizar Notas")
        else:
            print("\n" + "━" * 60)
            print("  CADASTRAR/ATUALIZAR NOTAS")
            print("━" * 60 + "\n")

        if hasattr(usuario, "obter_cadeiras"):
            cadeiras = usuario.obter_cadeiras()
        elif isinstance(usuario, dict):
            cadeiras = usuario.get("cadeiras", [])
        else:
            cadeiras = []

        if not cadeiras:
            self._print("Nenhuma cadeira cadastrada. Cadastre uma cadeira primeiro.")
            return

        self._print("Selecione a cadeira:")
        print()
        for i, cad in enumerate(cadeiras, 1):
            if isinstance(cad, dict):
                nome = cad.get("nome_cadeira") or cad.get("nome") or "Sem nome"
            else:
                nome = getattr(cad, "nome_cadeira", "Sem nome")
            print(f"  [{i}] {nome}")
        
        print()
        
        try:
            escolha = int(self._input("Número da cadeira"))
            if not (1 <= escolha <= len(cadeiras)):
                if self.console and hasattr(self.console, "exibir_erro"):
                    self.console.exibir_erro("Número inválido")
                else:
                    print("\n  ✗ Número inválido")
                return
        except Exception:
            if self.console and hasattr(self.console, "exibir_erro"):
                self.console.exibir_erro("Entrada inválida")
            else:
                print("\n  ✗ Entrada inválida")
            return

        cadeira_selecionada = cadeiras[escolha - 1]
        
        if isinstance(cadeira_selecionada, dict):
            codigo = cadeira_selecionada.get("codigo") or cadeira_selecionada.get("nome_cadeira")
        else:
            codigo = getattr(cadeira_selecionada, "codigo", None) or getattr(cadeira_selecionada, "nome_cadeira", None)

        print()
        self._print("📝 Digite as notas (deixe em branco se não tiver):")
        print()

        va1_str = self._input("VA1 (0-10)")
        va2_str = self._input("VA2 (0-10)")
        va3_str = self._input("VA3 (0-10)")
        rec_str = self._input("Recuperação (0-10, opcional)")

        def to_float_or_none(s):
            try:
                if not s or s.strip() == "":
                    return None
                return float(s)
            except Exception:
                return None

        va1 = to_float_or_none(va1_str)
        va2 = to_float_or_none(va2_str)
        va3 = to_float_or_none(va3_str)
        rec = to_float_or_none(rec_str)

        notas_dict = {
            "va1": va1,
            "va2": va2,
            "va3": va3,
            "recuperacao": rec
        }

        if isinstance(usuario, dict):
            nome_usuario = usuario.get("usuario") or usuario.get("nome")
        else:
            nome_usuario = getattr(usuario, "usuario", getattr(usuario, "nome", None))

        if not nome_usuario:
            if self.console and hasattr(self.console, "exibir_erro"):
                self.console.exibir_erro("Não foi possível identificar o usuário")
            else:
                print("\n  ✗ Erro")
            return

        try:
            ok = self.servico.atualizar_notas(nome_usuario, codigo, notas_dict)
            if ok:
                if self.console and hasattr(self.console, "exibir_sucesso"):
                    self.console.exibir_sucesso("Notas cadastradas com sucesso!")
                else:
                    print("\n  ✓ Notas cadastradas com sucesso!")
            else:
                if self.console and hasattr(self.console, "exibir_erro"):
                    self.console.exibir_erro("Falha ao cadastrar notas")
                else:
                    print("\n  ✗ Falha ao cadastrar notas")
        except Exception as e:
            if self.console and hasattr(self.console, "exibir_erro"):
                self.console.exibir_erro(f"Erro ao cadastrar notas: {e}")
            else:
                print(f"\n  ✗ Erro: {e}")