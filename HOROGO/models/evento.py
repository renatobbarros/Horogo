from typing import List, Dict, Any, Optional


class Evento:
    def __init__(self, titulo: str, data: str, local: str,descricao: str, participantes: Optional[List[str]] = None):
        self.titulo = titulo
        self.data = data
        self.local = local
        self.descricao = descricao
        self.participantes = participantes if participantes is not None else []

    def adicionar_participante(self, nome_usuario: str):
        if nome_usuario and nome_usuario not in self.participantes:
            self.participantes.append(nome_usuario)

    def remover_participante(self, nome_usuario: str):
        if nome_usuario in self.participantes:
            self.participantes.remove(nome_usuario)

    def obter_participantes(self) -> List[str]:
        return self.participantes

    def to_dict(self) -> Dict[str, Any]:
        return {
            "titulo": self.titulo,
            "data": self.data,
            "local": self.local,
            "descricao": self.descricao,
            "participantes": self.participantes
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Evento":
        if data is None:
            raise ValueError("data não pode ser None")
        return cls(
            titulo=data.get("titulo") or "",
            data=data.get("data") or "",
            local=data.get("local") or "",
            descricao=data.get("descricao") or "",
            participantes=data.get("participantes") or []
        )