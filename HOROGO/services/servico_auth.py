from ..repository.repositorio_usuario import repositorio_usuario
from ..models.usuario import Usuario


class Servico_Auth:
    """serviço de autenticação e gerenciamento de usuários."""
    def __init__(self, repositorio: repositorio_usuario):
        self.repositorio = repositorio

    def login(self, nome_usuario: str, senha: str):
        # retorna o objeto usuario em caso de sucesso, ou None em caso de falha.
        usuario_obj = self.repositorio.encontrar_usuario(nome_usuario)
        if usuario_obj and usuario_obj.verificar_senha(senha):
            return usuario_obj
        return None

    def registrar_usuario(self, nome: str, senha: str, instituicao: str, periodo):
        """Valida dados, cria e salva um novo usuário. Retorna o objeto Usuario em sucesso ou uma string com a mensagem de erro."""
        # Validações básicas conforme especificado nas instruções
        if not (0 < len(nome) <= 20):
            return "Erro: Nome de usuário inválido."
        if not (0 < len(senha) <= 12):
            return "Erro: Senha inválida."
        if self.repositorio.encontrar_usuario(nome):
            return "Erro: Usuário já existe."
        if not (str(periodo).isdigit() and 0 < int(periodo) <= 15):
            return "Erro: Período inválido."

        novo_usuario = Usuario(nome, senha, instituicao, int(periodo))
        self.repositorio.salvar_usuario(novo_usuario)
        return novo_usuario

    def redefinir_senha(self, nome_usuario: str, senha_nova: str, senha_confirmacao: str):
        """Redefine a senha de um usuário existente. Retorna o usuário atualizado em sucesso ou uma string de erro."""
        if senha_nova != senha_confirmacao:
            return "Erro: Senhas não conferem."
        if not (0 < len(senha_nova) <= 12):
            return "Erro: Senha inválida."

        usuario_obj = self.repositorio.encontrar_usuario(nome_usuario)
        if not usuario_obj:
            return "Erro: Usuário não encontrado."

        usuario_obj.senha = senha_nova
        self.repositorio.salvar_usuario(usuario_obj)
        return usuario_obj