import json
import os
from typing import List, Dict, Any

from ..models.tarefa import Tarefa
from ..models.data_importante import DataImportante


class servico_calendario:
    def __init__(self, caminho_json: str = None):
        # por padrão usa pasta HOROGO/Dados/eventos.json
        if caminho_json:
            self.caminho = caminho_json
        else:
            base = os.path.dirname(os.path.dirname(__file__))
            self.caminho = os.path.join(base, "Dados", "eventos.json")
        self.tarefas: List[Tarefa] = []
        self.datas: List[DataImportante] = []
        self._carregar()

    def _carregar(self):
        pasta = os.path.dirname(self.caminho) or "."
        os.makedirs(pasta, exist_ok=True)
        if not os.path.exists(self.caminho):
            try:
                with open(self.caminho, "w", encoding="utf-8") as f:
                    json.dump({"tarefas": [], "datas": []}, f, ensure_ascii=False, indent=4)
            except Exception:
                pass
            self.tarefas = []
            self.datas = []
            return

        try:
            with open(self.caminho, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {"tarefas": [], "datas": []}

        # Suporta arquivos legados que eram apenas uma lista de tarefas
        if isinstance(data, list):
            tarefas_list = [d for d in data if isinstance(d, dict)]
            datas_list = []
        elif isinstance(data, dict):
            tarefas_list = data.get("tarefas", []) if isinstance(data.get("tarefas", []), list) else []
            datas_list = data.get("datas", []) if isinstance(data.get("datas", []), list) else []
        else:
            tarefas_list = []
            datas_list = []

        self.tarefas = [Tarefa.from_dict(d) for d in tarefas_list if isinstance(d, dict)]
        self.datas = [DataImportante.from_dict(d) for d in datas_list if isinstance(d, dict)]

    def _salvar(self):
        out = {"tarefas": [t.to_dict() for t in self.tarefas], "datas": [d.to_dict() for d in self.datas]}
        try:
            with open(self.caminho, "w", encoding="utf-8") as f:
                json.dump(out, f, ensure_ascii=False, indent=4)
        except Exception:
            pass

    # Tarefas
    def adicionar_tarefa(self, titulo: str, tipo: str, data_iso: str, xp: int = None) -> Tarefa:
        if xp is None:
            xp = 10 if tipo == "trabalho" else 5 if tipo == "atividade" else 3
        t = Tarefa(titulo, tipo, data_iso, xp)
        self.tarefas.append(t)
        self._salvar()
        return t

    def listar_tarefas(self) -> List[Tarefa]:
        return list(self.tarefas)

    def marcar_tarefa_concluida(self, index: int) -> int:
        if 0 <= index < len(self.tarefas):
            t = self.tarefas.pop(index)
            self._salvar()
            return int(getattr(t, "xp", 0))
        return 0

    # Datas importantes
    def adicionar_data_importante(self, nome: str, data_iso: str, xp: int = 10) -> DataImportante:
        d = DataImportante(nome, data_iso, xp)
        self.datas.append(d)
        self._salvar()
        return d

    def listar_datas_importantes(self) -> List[DataImportante]:
        return list(self.datas)

    def marcar_data_concluida(self, index: int) -> int:
        if 0 <= index < len(self.datas):
            d = self.datas.pop(index)
            self._salvar()
            return int(getattr(d, "xp", 0))
        return 0
