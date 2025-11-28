from math import ceil
from typing import Iterable


class InterfaceAcademica:
    
    def __init__(self, console=None, col_width: int = 40):
        self.console = console
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