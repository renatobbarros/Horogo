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
        """Menu para cadastrar uma nova cadeira para o usuário.

        - coleta `nome`, `codigo`, `periodo`, `professor` e `tempo` via `self.console`;
        - usa `self.servico.criar_nova_cadeira` para construir a cadeira (dict);
        - adiciona campos extras (`nome_professor`, `tempo_cadeira`) e chama
          `self.servico.adicionar_cadeira_ao_usuario(nome_usuario, cadeira)`;
        - retorna True se salvo com sucesso, False caso contrário.
        """
        if not self.servico:
            self._print("Serviço acadêmico não configurado.")
            return False

        # determina o nome de usuário a partir do objeto passado
        nome_usuario = None
        try:
            # Usuario model ou dict
            if hasattr(usuario, "usuario"):
                nome_usuario = usuario.usuario
            elif isinstance(usuario, dict):
                nome_usuario = usuario.get("usuario") or usuario.get("nome")
            else:
                nome_usuario = str(usuario)
        except Exception:
            nome_usuario = str(usuario)

        # coleta dados via console (fallback para input)
        try:
            nome = self.console.obter_input("Nome da cadeira:")
        except Exception:
            nome = input("Nome da cadeira: ")
        if not nome:
            self._print("Nome inválido.")
            return False

        try:
            codigo = self.console.obter_input("Código da cadeira (ou ident):")
        except Exception:
            codigo = input("Código da cadeira (ou ident): ")

        try:
            periodo = self.console.obter_input("Período/semestre (número):")
        except Exception:
            periodo = input("Período/semestre (número): ")

        try:
            professor = self.console.obter_input("Nome do professor (opcional):")
        except Exception:
            professor = input("Nome do professor (opcional): ")

        try:
            tempo = self.console.obter_input("Carga horária (horas) (opcional):")
        except Exception:
            tempo = input("Carga horária (horas) (opcional): ")

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