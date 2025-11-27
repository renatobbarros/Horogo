# ...existing code...
from math import ceil

class InterfaceAcademica:
    def __init__(self, console=None, col_width=40):
        """
        console: instância opcional da InterfaceConsole (ou qualquer objeto com exibir_mensagem(str))
        col_width: largura da coluna esquerda (ajuste conforme terminal)
        """
        self.console = console
        self.col_width = col_width

    def _repr_item(self, item):
        if isinstance(item, dict):
            nome = item.get('nome') or item.get('name') or ""
            codigo = item.get('codigo') or item.get('code')
            return f"{nome} ({codigo})" if codigo else nome or str(item)
        return str(item)

    def listar_cadeiras_duas_colunas(self, cadeiras):
        """
        Exibe cadeiras em 2 colunas.
        cadeiras: lista de strings ou dicts (com 'nome' e opcional 'codigo')
        """
        n = len(cadeiras)
        if n == 0:
            self._print("Nenhuma cadeira encontrada.")
            return

        rows = ceil(n / 2)
        left_items = [self._repr_item(c) for c in cadeiras[:rows]]
        right_items = [self._repr_item(c) for c in cadeiras[rows:]]
        right_items += [""] * (rows - len(right_items))

        for l, r in zip(left_items, right_items):
            line = f"{l.ljust(self.col_width)}  {r}"
            self._print(line)

    def _print(self, texto):
        if self.console and hasattr(self.console, "exibir_mensagem"):
            try:
                self.console.exibir_mensagem(texto)
                return
            except Exception:
                pass
        print(texto)