class Cadeira:
    def __init__(self, nome_cadeira, nome_professor, tempo_cadeira, notas=None):
        self.nome_cadeira = nome_cadeira
        self.nome_professor = nome_professor
        self.tempo_cadeira = tempo_cadeira
        self.notas = notas 

    def adicionar_notas(self, va1, va2, va3):
        # self.notas = Nota(va1, va2, va3)
        pass

    def get_notas_formatadas(self) -> str:
        """retorna uma string formatada para exibição no console."""
        if not self.notas:
            return "Notas não cadastradas."
        
        v1 = self.notas.va1
        v2 = self.notas.va2
        v3 = self.notas.va3 if self.notas.va3 is not None else "N/A"

        # ele vai ficar assim:
        # VA1: (nota)
        # VA2: (nota)
        # VA3: (nota)
        return f"Nota VA1: {v1}\nNota VA2: {v2}\nNota VA3 (Final): {v3}"

    def obter_situacao(self) -> str:
        """Retorna a situação do aluno na cadeira. Por enquanto, ta so """
        if not self.notas:
            return "(CADASTRAR NOTA)"
        return "Aprovado"

    def to_dict(self) -> dict:
        """
        Converte a Cadeira para dicionário JSON.
        Se tiver notas, pede para o objeto Nota se converter também.
        """
        dados = {
            "nome_cadeira": self.nome_cadeira,
            "nome_professor": self.nome_professor,
            "tempo_cadeira": self.tempo_cadeira,
            "notas": None
        }
        
        # Se existir um objeto Nota, converte ele para dicionário
        if self.notas:
            dados["notas"] = self.notas.to_dict()
        return dados

    @classmethod
    def from_dict(cls, data: dict):
        dados_notas = data.get("notas")
        objeto_nota = None

        if dados_notas:
            objeto_nota = Nota.from_dict(dados_notas)

        return cls(
            nome_cadeira=data.get("nome_cadeira"),
            nome_professor=data.get("nome_professor"),
            tempo_cadeira=data.get("tempo_cadeira"),
            notas=objeto_nota 
        )