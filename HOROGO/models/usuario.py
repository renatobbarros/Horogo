from .cadeira import Cadeira


class Usuario:
    # seguir tudo das instruções da refatoração.
    def __init__(self, usuario, senha, instituicao, periodo, xp=0, nivel=1, cadeiras=None):
        self.usuario = usuario
        self.senha = senha
        self.instituicao = instituicao
        self.periodo = periodo
        self.xp = xp
        self.nivel = nivel

        # se cadeiras estiver vazia, cria uma lista vazia. caso contrario, puxar essa cadeira.
        self.cadeiras = cadeiras if cadeiras is not None else []


    def verificar_senha(self, senha_input: str) -> bool:
        """Retorna True se a senha fornecida bater com a senha do usuário.

        Usa `strip()` para ignorar espaços acidentais. Se `senha_input` for None,
        retorna False.
        """
        if senha_input is None:
            return False
        return self.senha == senha_input.strip()

    def adicionar_cadeira(self, cadeira_obj: Cadeira):
        """Adiciona uma `Cadeira` ao usuário"""
        if cadeira_obj is None:
            return

        if isinstance(cadeira_obj, dict):
            cadeira_obj = Cadeira.from_dict(cadeira_obj)

        if not isinstance(cadeira_obj, Cadeira):
            raise TypeError("adicionar_cadeira espera um Cadeira ou dict")

        self.cadeiras.append(cadeira_obj)

    def obter_cadeiras(self):
        return self.cadeiras

    def to_dict(self):
        """Serializa o Usuário para um dicionário (pronto para JSON).

        Converte também cada `Cadeira` usando seu `to_dict` quando aplicável.
        """
        return {
            "usuario": self.usuario,
            "senha": self.senha,
            "instituicao": self.instituicao,
            "periodo": self.periodo,
            "xp": self.xp,
            "nivel": self.nivel,
            "cadeiras": [c.to_dict() if hasattr(c, "to_dict") else c for c in self.cadeiras]
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Cria um `Usuario` a partir de um dicionário serializado."""
        cadeiras_data = data.get("cadeiras") or []
        cadeiras_objs = []

        for c in cadeiras_data:
            if isinstance(c, dict):
                cadeiras_objs.append(Cadeira.from_dict(c))
            else:
                cadeiras_objs.append(c)

        return cls(
            usuario=data.get("usuario"),
            senha=data.get("senha"),
            instituicao=data.get("instituicao"),
            periodo=data.get("periodo"),
            xp=data.get("xp", 0),
            nivel=data.get("nivel", 1),
            cadeiras=cadeiras_objs
        )