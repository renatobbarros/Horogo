from typing import Dict, Any
from datetime import datetime


class DataImportante:
    def __init__(self, nome: str, data_iso: str, xp: int = 10):
        self.nome = nome
        self.data_iso = data_iso
        self.xp = xp

    def to_dict(self) -> Dict[str, Any]:
        return {"nome": self.nome, "data_iso": self.data_iso, "xp": self.xp}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        if data is None:
            raise ValueError("data não pode ser None")
        return cls(nome=data.get("nome", ""), data_iso=data.get("data_iso", ""), xp=int(data.get("xp", 10)))

    def tempo_restante(self) -> str:
        try:
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
