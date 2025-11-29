from typing import List, Any
from datetime import datetime

from ..repository.repositorio_evento import RepositorioEvento
from ..repository.repositorio_usuario import repositorio_usuario
from ..models.evento import Evento


class ServicoMural:
    """Serviço de mural para gerenciar eventos e check-ins."""

    def __init__(self, repositorio_evento: RepositorioEvento, repositorio_usuario: repositorio_usuario):
        self.repo_evento = repositorio_evento
        self.repo_usuario = repositorio_usuario

    def validar_data(self, data_str: str) -> bool:
        try:
            datetime.strptime(data_str, "%Y-%m-%d")
            return True
        except Exception:
            return False

    def validar_evento(self, titulo: str, data: str, local: str, descricao: str) -> str:
        """Retorna string vazia se OK, ou mensagem de erro."""
        if not titulo or not isinstance(titulo, str):
            return "Título inválido"
        if len(titulo.strip()) < 3:
            return "Título deve ter pelo menos 3 caracteres"
        if len(titulo) > 100:
            return "Título muito longo (máximo 100 caracteres)"

        if not data or not isinstance(data, str):
            return "Data inválida"
        if not self.validar_data(data):
            return "Data deve estar no formato YYYY-MM-DD (ex: 2025-12-31)"

        if not local or not isinstance(local, str):
            return "Local inválido"
        if len(local.strip()) < 3:
            return "Local deve ter pelo menos 3 caracteres"
        if len(local) > 100:
            return "Local muito longo (máximo 100 caracteres)"

        if not descricao or not isinstance(descricao, str):
            return "Descrição inválida"
        if len(descricao.strip()) < 5:
            return "Descrição deve ter pelo menos 5 caracteres"
        if len(descricao) > 500:
            return "Descrição muito longa (máximo 500 caracteres)"

        return ""

    def criar_evento(self, titulo: str, data: str, local: str, descricao: str) -> Any:
        """Cria e adiciona um novo evento após validação."""
        erro = self.validar_evento(titulo, data, local, descricao)
        if erro:
            return f"Erro: {erro}"

        try:
            novo_evento = Evento(
                titulo=titulo.strip(),
                data=data.strip(),
                local=local.strip(),
                descricao=descricao.strip(),
                participantes=[]
            )
            self.repo_evento.adicionar_evento(novo_evento)
            return novo_evento
        except Exception as e:
            return f"Erro ao criar evento: {e}"

    def listar_eventos_disponiveis(self) -> List[Evento]:
        """Retorna eventos futuros (data >= hoje)."""
        todos = self.repo_evento.listar_eventos()
        hoje = datetime.now().date()
        
        eventos_futuros = []
        for e in todos:
            try:
                if isinstance(e, Evento):
                    data_evento = datetime.strptime(e.data, "%Y-%m-%d").date()
                    if data_evento >= hoje:
                        eventos_futuros.append(e)
                elif isinstance(e, dict):
                    data_str = e.get("data", "")
                    data_evento = datetime.strptime(data_str, "%Y-%m-%d").date()
                    if data_evento >= hoje:
                        eventos_futuros.append(Evento.from_dict(e))
            except Exception:
                continue
        
        return eventos_futuros

    def realizar_checkin(self, nome_usuario: str, titulo_evento: str) -> bool:
        if not nome_usuario or not titulo_evento:
            return False

        evento = self.repo_evento.encontrar_evento(titulo_evento)
        if not evento:
            return False

        usuario = self.repo_usuario.encontrar_usuario(nome_usuario)
        if not usuario:
            return False

        if isinstance(evento, Evento):
            evento.adicionar_participante(nome_usuario)
        else:
            participantes = evento.get("participantes", [])
            if nome_usuario not in participantes:
                participantes.append(nome_usuario)
            evento["participantes"] = participantes

        self.repo_evento._salvar_json()
        return True