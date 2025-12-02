from typing import Dict, Any
from datetime import datetime


class Tarefa:
    """dados de tarefas no JSON, incluindo adicionar esses dados pro dicionario."""
    def __init__(self, titulo: str, tipo: str, data_iso: str, xp: int = 5):
        self.titulo = titulo
        self.tipo = tipo  # e.g. 'trabalho', 'atividade', 'palestra'
        self.data_iso = data_iso  # string no formato ISO YYYY-MM-DD or full datetime
        self.xp = xp

    def to_dict(self) -> Dict[str, Any]:
        return {
            "titulo": self.titulo,
            "tipo": self.tipo,
            "data_iso": self.data_iso,
            "xp": self.xp,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        if data is None:
            raise ValueError("data não pode ser None")
        return cls(
            titulo=data.get("titulo", ""),
            tipo=data.get("tipo", "atividade"),
            data_iso=data.get("data_iso", ""),
            xp=int(data.get("xp", 5)),
        )

    def tempo_restante(self) -> str:
        try:
            # tenta interpretar data_iso (YYYY-MM-DD ou full ISO)
            dt = datetime.fromisoformat(self.data_iso)
        except Exception:
            try:
                dt = datetime.strptime(self.data_iso, "%Y-%m-%d")
            except Exception:
                return "data inválida"

        now = datetime.now()
        delta = dt - now
        if delta.total_seconds() < 0:
            return "já passou"
        days = delta.days
        hours = delta.seconds // 3600
        if days > 0:
            return f"{days} dia(s) e {hours} hora(s)"
        if hours > 0:
            return f"{hours} hora(s)"
        minutes = (delta.seconds % 3600) // 60
        return f"{minutes} minuto(s)"
