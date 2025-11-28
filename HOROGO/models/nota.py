# Versão simples (estudante iniciante/intermediário)

from typing import Optional, Dict, Any


class Nota:
    def __init__(self, va1: Optional[float], va2: Optional[float], va3: Optional[float], recuperacao: Optional[float]):
        def to_float(x):
            try:
                if x is None:
                    return None
                return float(x)
            except Exception:
                return None

        self.va1 = to_float(va1)
        self.va2 = to_float(va2)
        self.va3 = to_float(va3)
        self.recuperacao = to_float(recuperacao)

    def calcular_media_parcial(self) -> float:
        # regras simples para média parcial:
        a, b, c = self.va1, self.va2, self.va3

        # se VA1 e VA2 existem, usar média entre eles
        if a is not None and b is not None:
            return (a + b) / 2.0

        # se VA1 falta, usar VA2 e VA3 quando possível
        if a is None and b is not None:
            if c is not None:
                return (b + c) / 2.0
            return b

        # se VA2 falta, usar VA1 e VA3 quando possível
        if b is None and a is not None:
            if c is not None:
                return (a + c) / 2.0
            return a

        # se só tiver VA3 ou só VA3 válida
        if c is not None:
            return c

        # fallback quando não há notas válidas
        return 0.0

    def calcular_media_final(self) -> float:
        parcial = self.calcular_media_parcial()
        if self.recuperacao is not None:
            return (parcial + self.recuperacao) / 2.0
        return parcial

    def get_situacao(self) -> str:
        media = self.calcular_media_final()
        if media >= 7.0:
            return "Aprovado"
        return "Reprovado"

    def to_dict(self) -> Dict[str, Optional[float]]:
        return {
            "va1": self.va1,
            "va2": self.va2,
            "va3": self.va3,
            "recuperacao": self.recuperacao,
            "media_parcial": self.calcular_media_parcial(),
            "media_final": self.calcular_media_final(),
            "situacao": self.get_situacao(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Nota":
        if data is None:
            return cls(None, None, None, None)
        return cls(
            data.get("va1"),
            data.get("va2"),
            data.get("va3"),
            data.get("recuperacao"),
        )




