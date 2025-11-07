import getpass
import time

from HOROGO.Modulos.utilitarios import limpar_terminal, salvar_conta, carregar_conta

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
    def from_dict(cls, dados):
        # cls nesse caso aqui e a classe de objeto de usuario. então ele ta retornand o dicinario como uma classe de Usuario.
        return cls(
            dados['usuario'],
            dados['senha'],
            dados['instituicao'],
            dados['periodo_atual']
        )
        
class Autenticacao:
    """Sistema de login e cadastro."""
    def __init__(self):
        self.usuarios = self._carregar_usuarios()

    def _carregar_usuarios(self):

        conta = carregar_conta()
        usuario_objeto = {}
        for usuario, dados in conta.items():
            usuario_objeto[usuario] = Usuario.from_dict(dados)
        return usuario_objeto

    def _salvar_usuario(self):
        conta = {}
        for usuario, usuario_objeto in self.usuarios.items():
            conta[usuario] = usuario_objeto.dicionario()
        salvar_conta(conta)
    
    


