from typing import Any
from ..repository.repositorio_usuario import repositorio_usuario
from ..models.usuario import Usuario


class ServicoPerfil:
    """Serviço para gerenciar perfil do usuário."""

    def __init__(self, repositorio: repositorio_usuario):
        self.repositorio = repositorio

    def atualizar_senha(self, nome_usuario: str, nova_senha: str) -> Any:
        """Valida e atualiza a senha do usuário."""
        if not nova_senha or not isinstance(nova_senha, str):
            return "Erro: Senha inválida"
        
        if len(nova_senha) < 4:
            return "Erro: Senha deve ter pelo menos 4 caracteres"
        
        if len(nova_senha) > 12:
            return "Erro: Senha muito longa (máximo 12 caracteres)"

        usuario = self.repositorio.encontrar_usuario(nome_usuario)
        if not usuario:
            return "Erro: Usuário não encontrado"

        usuario.senha = nova_senha.strip()
        try:
            self.repositorio.salvar_usuario(usuario)
            return usuario
        except Exception as e:
            return f"Erro ao salvar senha: {e}"

    def atualizar_instituicao(self, nome_usuario: str, nova_instituicao: str) -> Any:
        if not nova_instituicao or not isinstance(nova_instituicao, str):
            return "Erro: Instituição inválida"
        
        if len(nova_instituicao.strip()) < 3:
            return "Erro: Instituição deve ter pelo menos 3 caracteres"
        
        if len(nova_instituicao) > 100:
            return "Erro: Nome da instituição muito longo (máximo 100 caracteres)"

        usuario = self.repositorio.encontrar_usuario(nome_usuario)
        if not usuario:
            return "Erro: Usuário não encontrado"

        usuario.instituicao = nova_instituicao.strip()
        try:
            self.repositorio.salvar_usuario(usuario)
            return usuario
        except Exception as e:
            return f"Erro ao salvar instituição: {e}"

    def atualizar_periodo(self, nome_usuario: str, novo_periodo: Any) -> Any:
        try:
            periodo_int = int(novo_periodo)
            if not (1 <= periodo_int <= 15):
                return "Erro: Período deve estar entre 1 e 15"
        except Exception:
            return "Erro: Período deve ser um número válido"

        usuario = self.repositorio.encontrar_usuario(nome_usuario)
        if not usuario:
            return "Erro: Usuário não encontrado"

        usuario.periodo = periodo_int
        try:
            self.repositorio.salvar_usuario(usuario)
            return usuario
        except Exception as e:
            return f"Erro ao salvar período: {e}"