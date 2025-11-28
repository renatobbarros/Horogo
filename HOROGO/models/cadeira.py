from typing import Optional, Any
from .nota import Nota


class Cadeira:

    def __init__(self, nome_cadeira: str, nome_professor: str, tempo_cadeira: Any, notas: Optional[Any] = None):
        self.nome_cadeira = nome_cadeira
        self.nome_professor = nome_professor
        self.tempo_cadeira = tempo_cadeira

        if isinstance(notas, dict):
            # converter dict para Nota (assume chaves va1, va2, va3, recuperacao)
            self.notas = Nota(
                notas.get("va1"),
                notas.get("va2"),
                notas.get("va3"),
                notas.get("recuperacao"),
            )
        elif isinstance(notas, Nota):
            self.notas = notas
        else:
            # pode ser None ou formato desconhecido
            self.notas = None

    def adicionar_notas(self, va1: Any, va2: Any = None, va3: Any = None, recuperacao: Any = None) -> Nota:
        """Cria ou atualiza o objeto Nota desta cadeira."""
        self.notas = Nota(va1, va2, va3, recuperacao)
        return self.notas

    def get_notas_formatadas(self) -> str:
        """Retorna uma string simples com as notas."""
        if not self.notas:
            return "Nenhuma nota cadastrada."
        # usa atributos do objeto Nota (assume nomes va1, va2, va3)
        v1 = getattr(self.notas, "va1", "N/A")
        v2 = getattr(self.notas, "va2", "N/A")
        v3 = getattr(self.notas, "va3", "N/A")
        rec = getattr(self.notas, "recuperacao", "N/A")
        return f"VA1: {v1}\nVA2: {v2}\nVA3: {v3}\nRecuperação: {rec}"

    def obter_situacao(self) -> str:
        """
        Retorna 'Aprovado' ou 'Reprovado' tentando usar calcular_media_final().
        """
        if not self.notas:
            return "Sem dados"
        if hasattr(self.notas, "calcular_media_final"):
            try:
                media = self.notas.calcular_media_final()
                return "Aprovado" if media >= 7 else "Reprovado"
            except Exception:
                return "Sem dados"
        return "Sem dados"

    def to_dict(self) -> dict:
        """Serializa a cadeira para dict (pronto para JSON)."""
        result = {
            "nome_cadeira": self.nome_cadeira,
            "nome_professor": self.nome_professor,
            "tempo_cadeira": self.tempo_cadeira,
            "notas": None,
        }
        if self.notas:
            if hasattr(self.notas, "to_dict"):
                result["notas"] = self.notas.to_dict()
            else:
                result["notas"] = {
                    "va1": getattr(self.notas, "va1", None),
                    "va2": getattr(self.notas, "va2", None),
                    "va3": getattr(self.notas, "va3", None),
                    "recuperacao": getattr(self.notas, "recuperacao", None),
                }
        return result

    @classmethod
    def from_dict(cls, data: dict):
        """Cria Cadeira a partir de dict."""
        if data is None:
            raise ValueError("data não pode ser None")
        notas = data.get("notas")
        if isinstance(notas, dict):
            notas_obj = Nota(
                notas.get("va1"),
                notas.get("va2"),
                notas.get("va3"),
                notas.get("recuperacao"),
            )
        else:
            notas_obj = None
        return cls(
            nome_cadeira=data.get("nome_cadeira") or data.get("nome") or "",
            nome_professor=data.get("nome_professor") or data.get("professor") or "",
            tempo_cadeira=data.get("tempo_cadeira"),
            notas=notas_obj,
        )