from typing import Optional, Any
from ..repository.repositorio_usuario import repositorio_usuario
from ..models.usuario import Usuario


class servico_auth:
    """tudo relacionado ao login do usuario e aqui. fazer login, registrar, redefinir senha, etc."""

    def __init__(self, repositorio: repositorio_usuario):
        self.repositorio = repositorio

    def login(self, nome_usuario: str, senha: str) -> Optional[Usuario]:
        """Retorna Usuario ou None se falhar."""
        if not nome_usuario or not senha:
            return None

        usuario = self.repositorio.encontrar_usuario(nome_usuario)
        if not usuario:
            return None

        try:
            if usuario.verificar_senha(senha):
                return usuario
        except Exception:
            return None

        return None

    def registrar_usuario(self, nome: str, senha: str, instituicao: str, periodo: Any) -> Any:
        if not nome or not isinstance(nome, str) or len(nome) > 20:
            return "Erro: Nome inválido."
        if not senha or not isinstance(senha, str) or len(senha) > 12:
            return "Erro: Senha inválida."
        if self.repositorio.encontrar_usuario(nome):
            return "Erro: Usuário já existe."

        try:
            periodo_int = int(periodo)
        except Exception:
            return "Erro: Período inválido."

        novo = Usuario(nome, senha, instituicao, periodo_int)
        try:
            self.repositorio.salvar_usuario(novo)
        except Exception as e:
            return f"Erro ao salvar usuário: {e}"
        return novo

    def redefinir_senha(self, nome_usuario: str, senha_nova: str, senha_confirmacao: str) -> Any:
        """Redefine a senha do usuário se as senhas conferirem."""
        if senha_nova != senha_confirmacao:
            return "Erro: Senhas não conferem."
        if not senha_nova or len(senha_nova) > 12:
            return "Erro: Senha inválida."

        usuario = self.repositorio.encontrar_usuario(nome_usuario)
        if not usuario:
            return "Erro: Usuário não encontrado."

        usuario.senha = senha_nova
        try:
            self.repositorio.salvar_usuario(usuario)
        except Exception as e:
            return f"Erro ao salvar nova senha: {e}"
        return usuario