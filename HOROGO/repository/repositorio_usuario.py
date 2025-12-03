import json
import os
from typing import Any

from ..models.usuario import Usuario


class repositorio_usuario:
    """repositório para usuários, armazenados em JSON."""
    def __init__(self, caminho_json: str):
        self.caminho_json = caminho_json
        self.usuarios = [] 
        self.carregar_usuarios()

    def carregar_usuarios(self) -> None:
        """Lê o arquivo JSON e converte em objetos Usuario."""
        if not os.path.exists(self.caminho_json):
            pasta = os.path.dirname(self.caminho_json) or "."
            os.makedirs(pasta, exist_ok=True)
            try:
                with open(self.caminho_json, "w", encoding="utf-8") as f:
                    json.dump([], f, ensure_ascii=False, indent=4)
            except Exception:
                pass
            self.usuarios = []
            return

        try:
            with open(self.caminho_json, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            self.usuarios = []
            return

        if not isinstance(data, list):
            self.usuarios = []
            return

        usuarios = []
        for item in data:
            if isinstance(item, dict):
                try:
                    u = Usuario.from_dict(item)
                except Exception:
                    nome = item.get("usuario") or item.get("nome") or ""
                    senha = item.get("senha") or ""
                    instituicao = item.get("instituicao")
                    periodo = item.get("periodo")
                    u = Usuario(nome, senha, instituicao, periodo, xp=item.get("xp", 0), nivel=item.get("nivel", 1), cadeiras=item.get("cadeiras", []))
                usuarios.append(u)
            elif isinstance(item, Usuario):
                usuarios.append(item)
        self.usuarios = usuarios

    def _salvar_json(self) -> None:
        """Serializa a lista de usuários e grava no JSON."""
        out = []
        for u in self.usuarios:
            if hasattr(u, "to_dict"):
                out.append(u.to_dict())
            elif isinstance(u, dict):
                out.append(u)
            else:
                try:
                    out.append(u.__dict__)
                except Exception:
                    pass

        pasta = os.path.dirname(self.caminho_json) or "."
        os.makedirs(pasta, exist_ok=True)
        try:
            with open(self.caminho_json, "w", encoding="utf-8") as f:
                json.dump(out, f, ensure_ascii=False, indent=4)
        except Exception:
            pass

    def encontrar_usuario(self, username: str) -> Any:
        """Procura usuário por nome."""
        if username is None:
            return None
        chave = str(username).strip()
        for u in self.usuarios:
            if isinstance(u, Usuario):
                if u.usuario == chave or getattr(u, "nome", None) == chave:
                    return u
            elif isinstance(u, dict):
                if u.get("usuario") == chave or u.get("nome") == chave:
                    try:
                        return Usuario.from_dict(u)
                    except Exception:
                        return None
        return None

    def salvar_usuario(self, usuario: Any) -> None:
        """Adiciona ou atualiza um usuário e grava no JSON."""
        if usuario is None:
            return

        try:
            if isinstance(usuario, dict):
                usuario_obj = Usuario.from_dict(usuario)
            elif isinstance(usuario, Usuario):
                usuario_obj = usuario
            else:
                raise TypeError(f"salvar_usuario espera dict ou Usuario, recebeu {type(usuario).__name__}")
        except Exception as e:
            raise TypeError(f"salvar_usuario espera dict ou Usuario, erro: {e}")

        existente = self.encontrar_usuario(usuario_obj.usuario)
        if existente:
            for i, u in enumerate(self.usuarios):
                if (isinstance(u, Usuario) and u.usuario == existente.usuario) or (isinstance(u, dict) and (u.get("usuario") == existente.usuario or u.get("nome") == existente.usuario)):
                    self.usuarios[i] = usuario_obj
                    break
        else:
            self.usuarios.append(usuario_obj)

        self._salvar_json()