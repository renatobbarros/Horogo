class Usuario:
    """A classe de Usuario na memoria do Python. Apenas representa um unico usuario, e não todos."""
    # Os comentarios aqui dentro depois vão ser perfurmados, mas por enquanto NÃO apague ate a gente entender como que funciona toda a obra.

    def __init__(self, usuario, senha, instituicao, periodo_atual):
        """informação do usuario, caso não e obvio o suficiente."""
        self.usuario = usuario.lower()
        self.senha = senha.lower()
        self.instituicao = instituicao.lower()
        self.periodo = int(periodo_atual)

    def senha_valida(self, entrada_senha):
        """se senha = entrada senha, retorna senha. se não, fudeu"""
        return self.senha == entrada_senha.strip()
    
    def dicionario(self):
        """retorna os dados como um dicionario, basicamente o mesmo processo de antes."""
        return {
            'usuario': self.usuario,
            'senha': self.senha,
            'instituição': self.instituicao,
            'periodo_atual': self.periodo_atual
        }

    # Esse daqui eu peguei do Gemini, pra entender. Depois eu faço minha propria versão, mas deixa aqui por enquanto so pra entender a logica.

    # Faz com que esse metodo seja algo para a classe, não para a instancia de uma classe. Ou basicamente vira uma função global para a classe.
    @classmethod
    def from_dict(cls, data):
        # cls nesse caso aqui e a classe de objeto de usuario. então ele ta retornand o dicinario como uma classe de Usuario.
        return cls(
            data['usuario'],
            data['senha'],
            data['instituicao'],
            data['periodo_atual']
        )
        