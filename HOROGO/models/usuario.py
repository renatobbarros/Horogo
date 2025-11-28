from typing import List, Optional, Dict, Any
from .cadeira import Cadeira


class Usuario:
    def __init__(
        self,
        usuario: str,
        senha: str,
        instituicao: str,
        periodo: Any,
        xp: int = 0,
        nivel: int = 1,
        cadeiras: Optional[List[Any]] = None,
    ):
        self.usuario = usuario
        self.senha = senha
        self.instituicao = instituicao
        self.periodo = periodo
        self.xp = int(xp) if xp is not None else 0
        self.nivel = int(nivel) if nivel is not None else 1
        self.cadeiras = cadeiras if cadeiras is not None else []

    def verificar_senha(self, senha_input: Optional[str]) -> bool:
        """Verifica senha"""
        if senha_input is None:
            return False
        return self.senha == senha_input.strip()

    def adicionar_cadeira(self, cadeira_obj: Any) -> None:
        """Adiciona uma cadeira"""
        if cadeira_obj is None:
            return
        if isinstance(cadeira_obj, dict):
            # tenta converter dict para Cadeira
            try:
                cadeira_obj = Cadeira.from_dict(cadeira_obj)
            except Exception:
                # se falhar, apenas guarda o dict
                self.cadeiras.append(cadeira_obj)
                return
        if isinstance(cadeira_obj, Cadeira):
            self.cadeiras.append(cadeira_obj)
        else:
            # se receber outro tipo, guarda como está
            self.cadeiras.append(cadeira_obj)

    def obter_cadeiras(self) -> List[Any]:
        """Retorna a lista de cadeiras"""
        return self.cadeiras

    def to_dict(self) -> Dict[str, Any]:
        """Serialize simples para JSON/dicionário."""
        cadeiras_serial = []
        for c in self.cadeiras:
            if hasattr(c, "to_dict"):
                cadeiras_serial.append(c.to_dict())
            else:
                cadeiras_serial.append(c)
        return {
            "usuario": self.usuario,
            "nome": self.usuario,
            "senha": self.senha,
            "instituicao": self.instituicao,
            "periodo": self.periodo,
            "xp": self.xp,
            "nivel": self.nivel,
            "cadeiras": cadeiras_serial,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Cria Usuario a partir de dicionário"""
        if data is None:
            raise ValueError("data não pode ser None")
        usuario = data.get("usuario") or data.get("nome") or ""
        senha = data.get("senha") or ""
        instituicao = data.get("instituicao")
        periodo = data.get("periodo")
        xp = data.get("xp", 0)
        nivel = data.get("nivel", 1)

        cadeiras_data = data.get("cadeiras") or []
        cadeiras = []
        for c in cadeiras_data:
            if isinstance(c, dict):
                try:
                    cadeiras.append(Cadeira.from_dict(c))
                except Exception:
                    cadeiras.append(c)
            else:
                cadeiras.append(c)

        return cls(usuario, senha, instituicao, periodo, xp=xp, nivel=nivel, cadeiras=cadeiras)