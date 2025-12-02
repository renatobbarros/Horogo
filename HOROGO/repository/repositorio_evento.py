import json
import os
from typing import List, Optional, Any

from ..models.evento import Evento


class RepositorioEvento:
    """mesma coisa do repositorio_usuario, mas para eventos."""
    def __init__(self, caminho_json: str):
        self.caminho_json = caminho_json
        self.eventos: List[Evento] = []
        self.carregar_eventos()

    def carregar_eventos(self) -> None:
        if not os.path.exists(self.caminho_json):
            self.eventos = []
            return

        try:
            with open(self.caminho_json, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            self.eventos = []
            return

        if not isinstance(data, list):
            self.eventos = []
            return

        eventos = []
        for item in data:
            if isinstance(item, dict):
                try:
                    eventos.append(Evento.from_dict(item))
                except Exception:
                    pass
            elif isinstance(item, Evento):
                eventos.append(item)
        self.eventos = eventos

    def _salvar_json(self) -> None:
        """Persiste lista de eventos como dicionários no arquivo JSON."""
        out = []
        for e in self.eventos:
            if hasattr(e, "to_dict"):
                out.append(e.to_dict())
            elif isinstance(e, dict):
                out.append(e)
            else:
                try:
                    out.append(e.__dict__)
                except Exception:
                    pass

        pasta = os.path.dirname(self.caminho_json) or "."
        os.makedirs(pasta, exist_ok=True)
        try:
            with open(self.caminho_json, "w", encoding="utf-8") as f:
                json.dump(out, f, ensure_ascii=False, indent=4)
        except Exception:
            pass

    def listar_eventos(self) -> List[Evento]:
        """Retorna todos os eventos."""
        return self.eventos

    def adicionar_evento(self, evento: Any) -> None:
        """Adiciona um novo evento."""
        if evento is None:
            return

        if isinstance(evento, dict):
            evento_obj = Evento.from_dict(evento)
        elif isinstance(evento, Evento):
            evento_obj = evento
        else:
            raise TypeError("adicionar_evento espera Evento ou dict")

        self.eventos.append(evento_obj)
        self._salvar_json()

    def remover_evento(self, titulo: str) -> bool:
        """Remove um evento pelo título. Retorna True se removeu."""
        for i, e in enumerate(self.eventos):
            if isinstance(e, Evento) and e.titulo == titulo:
                del self.eventos[i]
                self._salvar_json()
                return True
            elif isinstance(e, dict) and e.get("titulo") == titulo:
                del self.eventos[i]
                self._salvar_json()
                return True
        return False

    def encontrar_evento(self, titulo: str) -> Optional[Evento]:
        """Procura um evento pelo título."""
        if not titulo:
            return None
        for e in self.eventos:
            if isinstance(e, Evento) and e.titulo == titulo:
                return e
            elif isinstance(e, dict) and e.get("titulo") == titulo:
                try:
                    return Evento.from_dict(e)
                except Exception:
                    pass
        return None