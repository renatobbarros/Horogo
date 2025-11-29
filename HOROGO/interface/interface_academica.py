from math import ceil
from typing import Iterable, Optional


class InterfaceAcademica:

    def __init__(self, console=None, horobot=None, servico=None, col_width: int = 40):
        self.console = console
        self.horobot = horobot
        self.servico = servico
        # largura fixa para a coluna esquerda
        self.col_width = int(col_width) if col_width and int(col_width) > 0 else 40

    def _repr_item(self, item) -> str:
        """Representa um item de cadeira como texto legível """
        if isinstance(item, dict):
            return item.get("nome") or item.get("name") or str(item)
        return str(item)

    def listar_cadeiras_duas_colunas(self, cadeiras: Iterable):
        """
        Mostra a lista de cadeiras em duas colunas simples.
        """
        if not cadeiras:
            self._print("Nenhuma cadeira encontrada.")
            return

        # garante que seja lista 
        try:
            cadeiras = list(cadeiras)
        except Exception:
            self._print("Formato inválido de cadeiras.")
            return

        n = len(cadeiras)
        rows = ceil(n / 2)

        esquerda = [self._repr_item(x) for x in cadeiras[:rows]]
        direita = [self._repr_item(x) for x in cadeiras[rows:]]
        # completa a direita para ter o mesmo número de linhas
        while len(direita) < rows:
            direita.append("")

        for l, r in zip(esquerda, direita):
            # recorta se muito longo e formata duas colunas
            if len(l) > self.col_width:
                l = l[: max(1, self.col_width - 3)] + "..."
            line = f"{l.ljust(self.col_width)}  {r}"
            self._print(line)

    def _print(self, texto: str):
        """Imprime via console se disponível, senão usa print()."""
        if self.console and hasattr(self.console, "exibir_mensagem"):
            try:
                self.console.exibir_mensagem(texto)
                return
            except Exception:
                pass
        print(texto)

    def executar_menu_cadastrar_cadeira(self, usuario) -> bool:
        """Menu para cadastrar uma nova cadeira para o usuário."""
        if not self.servico:
            self._print("Serviço acadêmico não configurado.")
            return False

        # determina o nome de usuário a partir do objeto passado
        nome_usuario = None
        try:
            # extrai nome_usuario, com um fallback para puxar de um dicionario
            if hasattr(usuario, "usuario"):
                nome_usuario = usuario.usuario
            elif isinstance(usuario, dict):
                nome_usuario = usuario.get("usuario") or usuario.get("nome")
            else:
                nome_usuario = str(usuario)
        except Exception:
            nome_usuario = str(usuario)

        # coleta dados via console (fallback para input) com reloops e opção de cancelar
        while True:
            try:
                nome = self.console.obter_input("Nome da cadeira (digite 0 para cancelar):")
            except Exception:
                nome = input("Nome da cadeira (digite 0 para cancelar): ")
            nome = str(nome or "").strip()
            if nome == "0":
                return False
            if not nome or len(nome) > 50:
                self._print("Nome inválido. Informe entre 1 e 50 caracteres.")
                continue
            break

        try:
            codigo = self.console.obter_input("Código da cadeira (ou ident, opcional):")
        except Exception:
            codigo = input("Código da cadeira (ou ident, opcional): ")
        codigo = None if codigo is None or str(codigo).strip() == "" else str(codigo).strip()

        while True:
            try:
                periodo = self.console.obter_input("Período/semestre (número) (digite 0 para cancelar):")
            except Exception:
                periodo = input("Período/semestre (número) (digite 0 para cancelar): ")
            periodo_str = str(periodo or "").strip()
            if periodo_str == "0":
                return False
            if not periodo_str.isdigit() or not (1 <= int(periodo_str) <= 15):
                self._print("Período inválido. Informe um número entre 1 e 15.")
                continue
            periodo = int(periodo_str)
            break

        try:
            professor = self.console.obter_input("Nome do professor (opcional, deixe em branco para pular):")
        except Exception:
            professor = input("Nome do professor (opcional, deixe em branco para pular): ")
        professor = None if professor is None or str(professor).strip() == "" else str(professor).strip()

        while True:
            try:
                tempo = self.console.obter_input("Carga horária (horas) (opcional, digite 0 para cancelar):")
            except Exception:
                tempo = input("Carga horária (horas) (opcional, digite 0 para cancelar): ")
            tempo_str = str(tempo or "").strip()
            if tempo_str == "0":
                return False
            if tempo_str == "":
                tempo = None
                break
            try:
                tempo_val = float(tempo_str)
                if tempo_val <= 0:
                    self._print("Carga horária deve ser maior que zero.")
                    continue
                tempo = tempo_val
                break
            except Exception:
                self._print("Carga horária inválida. Informe um número (ex: 40) ou deixe em branco.")
                continue

        # valida periodo localmente antes de chamar o serviço
        periodo_str = str(periodo).strip()
        if not periodo_str.isdigit() or not (1 <= int(periodo_str) <= 15):
            self._print("Período inválido. Informe um número entre 1 e 15.")
            return False

        # valida carga horária opcional (se preenchida deve ser número positivo)
        tempo_str = str(tempo).strip()
        if tempo_str != "":
            try:
                tempo_val = float(tempo_str)
                if tempo_val <= 0:
                    self._print("Carga horária deve ser maior que zero.")
                    return False
            except Exception:
                self._print("Carga horária inválida. Informe um número.")
                return False

        # criar cadeira via serviço
        try:
            cadeira = self.servico.criar_nova_cadeira(nome, codigo, periodo)
            # acrescenta campos extras se não existirem
            if isinstance(cadeira, dict):
                cadeira["nome_professor"] = professor
                cadeira["tempo_cadeira"] = tempo
        except Exception as e:
            self._print(f"Erro ao criar cadeira: {e}")
            return False

        # adiciona ao usuário
        try:
            sucesso = self.servico.adicionar_cadeira_ao_usuario(nome_usuario, cadeira)
        except Exception as e:
            self._print(f"Erro ao salvar cadeira: {e}")
            return False

        if sucesso:
            self._print("Cadeira cadastrada com sucesso.")
            return True
        else:
            self._print("Falha ao cadastrar a cadeira.")
            return False

    def executar_menu_cadastrar_notas(self, usuario) -> bool:
        """Menu para cadastrar/atualizar notas de uma cadeira do usuário."""
        if not self.servico:
            self._print("Serviço acadêmico não configurado.")
            return False

        # extrai nome_usuario
        if hasattr(usuario, "usuario"):
            nome_usuario = usuario.usuario
        elif isinstance(usuario, dict):
            nome_usuario = usuario.get("usuario") or usuario.get("nome")
        else:
            nome_usuario = str(usuario)

        # obter lista de cadeiras
        if hasattr(usuario, "obter_cadeiras"):
            cadeiras = usuario.obter_cadeiras()
        elif isinstance(usuario, dict):
            cadeiras = usuario.get("cadeiras", [])
        else:
            cadeiras = []

        if not cadeiras:
            self._print("Você não tem cadeiras cadastradas. Cadastre uma antes." )
            return False

        # apresenta lista simples com índices
        self._print("Escolha a cadeira para cadastrar notas:")
        for i, c in enumerate(cadeiras, start=1):
            nome = c.get("nome_cadeira") if isinstance(c, dict) else getattr(c, "nome_cadeira", getattr(c, "nome", str(c)))
            codigo = c.get("codigo") if isinstance(c, dict) else getattr(c, "codigo", None)
            display = f"[{i}] {nome}"
            if codigo:
                display += f" (id: {codigo})"
            self._print(display)

        # escolha da cadeira com reloop e possibilidade de cancelar (0)
        while True:
            try:
                escolha_txt = self.console.obter_input("Digite o número da cadeira (ou 0 para cancelar):")
            except Exception:
                escolha_txt = input("Digite o número da cadeira (ou 0 para cancelar): ")

            try:
                escolha = int(str(escolha_txt).strip())
            except Exception:
                self._print("Entrada inválida. Digite o número correspondente à cadeira ou 0 para cancelar.")
                continue

            if escolha == 0:
                return False
            if 1 <= escolha <= len(cadeiras):
                break
            self._print("Escolha inválida. Tente novamente.")

        cad = cadeiras[escolha - 1]
        # identifica código da cadeira
        codigo = None
        if isinstance(cad, dict):
            codigo = cad.get("codigo") or cad.get("nome_cadeira") or cad.get("nome")
        else:
            codigo = getattr(cad, "codigo", None) or getattr(cad, "nome_cadeira", None) or getattr(cad, "nome", None)

        # coleta notas com reloops. Digite 'C' para cancelar a operação a qualquer momento.
        def _ask_note(prompt):
            while True:
                try:
                    txt = self.console.obter_input(f"{prompt} (ou deixe em branco) [C para cancelar]:")
                except Exception:
                    txt = input(f"{prompt} (ou deixe em branco) [C para cancelar]: ")
                if txt is None:
                    return None
                s = str(txt).strip()
                if s.upper() == 'C':
                    return 'CANCEL'
                if s == "":
                    return None
                try:
                    v = float(s)
                except Exception:
                    self._print("Valor inválido. Informe um número (0-10) ou deixe em branco.")
                    continue
                if not (0.0 <= v <= 10.0):
                    self._print("Nota fora do intervalo 0-10.")
                    continue
                return v

        va1 = _ask_note("VA1")
        if va1 == 'CANCEL':
            return False
        va2 = _ask_note("VA2")
        if va2 == 'CANCEL':
            return False
        va3 = _ask_note("VA3")
        if va3 == 'CANCEL':
            return False

        lista_notas = {
            "va1": va1,
            "va2": va2,
            "va3": va3,
            "recuperacao": None,
        }

        # valida notas: cada nota, se fornecida, deve ser 0 <= nota <= 10
        def _validar_valor(v):
            if v is None:
                return True
            try:
                f = float(v)
            except Exception:
                return False
            return 0.0 <= f <= 10.0

        if not (_validar_valor(lista_notas["va1"]) and _validar_valor(lista_notas["va2"]) and _validar_valor(lista_notas["va3"])):
            self._print("Valores de notas inválidos. Informe números entre 0 e 10 (ou deixe em branco).")
            return False

        # chama serviço para atualizar
        try:
            sucesso = self.servico.atualizar_notas(nome_usuario, codigo, lista_notas)
        except Exception as e:
            self._print(f"Erro ao atualizar notas: {e}")
            return False

        if sucesso:
            self._print("Notas atualizadas com sucesso.")
            return True
        else:
            self._print("Falha ao atualizar notas.")
            return False

    def executar_situacao_cadeiras(self, usuario):
        """Exibe a situação formatada de cada cadeira do usuário."""
        # pega cadeiras
        if hasattr(usuario, "obter_cadeiras"):
            cadeiras = usuario.obter_cadeiras()
        elif isinstance(usuario, dict):
            cadeiras = usuario.get("cadeiras", [])
        else:
            cadeiras = []

        if not cadeiras:
            self._print("Você não tem cadeiras cadastradas.")
            return

        # para cada cadeira, tenta exibir notas e situação
        from ..models.nota import Nota

        for i, c in enumerate(cadeiras, start=1):
            if isinstance(c, dict):
                nome = c.get("nome_cadeira") or c.get("nome") or f"Cadeira {i}"
                notas = c.get("notas")
                self._print(f"----- CADEIRA {i}: {nome} -----")
                if notas:
                    try:
                        n = Nota.from_dict(notas) if hasattr(Nota, "from_dict") else None
                        if n:
                            self._print(n.get_situacao())
                        else:
                            self._print(str(notas))
                    except Exception:
                        self._print(str(notas))
                else:
                    self._print("Notas não cadastradas.")
            else:
                nome = getattr(c, "nome_cadeira", getattr(c, "nome", f"Cadeira {i}"))
                self._print(f"----- CADEIRA {i}: {nome} -----")
                try:
                    self._print(c.get_notas_formatadas())
                except Exception:
                    self._print("Notas não cadastradas.")
                try:
                    # usa método do modelo
                    situ = c.obter_situacao() if hasattr(c, "obter_situacao") else "Indefinida"
                    self._print(f"Situação: {situ}")
                except Exception:
                    self._print("Situação: Indefinida")