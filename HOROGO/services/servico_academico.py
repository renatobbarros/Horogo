from typing import Any, Union
from ..repository.repositorio_usuario import repositorio_usuario
from ..models.usuario import Usuario
from ..models.cadeira import Cadeira
from ..models.nota import Nota


class servico_academico:
    def __init__(self, repositorio: repositorio_usuario):
        # guarda o repositório para usar depois
        self.repositorio = repositorio

    def criar_nova_cadeira(self, nome_cadeira: str, codigo_cadeira: str, periodo: Any) -> dict:
        '''cria um dicionário simples representando a cadeira'''
        return {
            "nome": nome_cadeira,
            "nome_cadeira": nome_cadeira,
            "codigo": codigo_cadeira,
            "periodo": periodo,
            "notas": None,
        }

    def adicionar_cadeira_ao_usuario(self, nome_usuario: str, cadeira: Union[dict, Cadeira]) -> bool:
        """adiciona uma cadeira""" 
        usuario = self.repositorio.encontrar_usuario(nome_usuario)
        if not usuario:
            return False

        # se veio um objeto Usuario, usa método do modelo
        if isinstance(usuario, Usuario):
            try:
                usuario.adicionar_cadeira(cadeira)
                self.repositorio.salvar_usuario(usuario)
                return True
            except Exception:
                return False

        # se for dict mantém estrutura de dicionários
        try:
            cadeiras = usuario.get("cadeiras") or []
            if isinstance(cadeira, Cadeira):
                # converte Cadeira para dict se possível
                cadeiras.append(cadeira.to_dict() if hasattr(cadeira, "to_dict") else {
                    "nome_cadeira": getattr(cadeira, "nome_cadeira", None),
                    "nome_professor": getattr(cadeira, "nome_professor", None),
                    "tempo_cadeira": getattr(cadeira, "tempo_cadeira", None),
                    "notas": getattr(cadeira, "notas", None),
                })
            else:
                cadeiras.append(cadeira)
            usuario["cadeiras"] = cadeiras
            self.repositorio.salvar_usuario(usuario)
            return True
        except Exception:
            return False

    def atualizar_notas(self, nome_usuario: str, codigo_cadeira: str, notas: Union[dict, Nota]) -> bool:
        """atualiza as notas de uma cadeira do usuário."""
        usuario = self.repositorio.encontrar_usuario(nome_usuario)
        if not usuario:
            return False

        # pega lista de cadeiras (objetos ou dicts)
        if isinstance(usuario, Usuario):
            cadeiras = usuario.cadeiras
        else:
            cadeiras = usuario.get("cadeiras", [])

        encontrado = False
        for idx, cad in enumerate(cadeiras):
            # tenta obter um identificador da cadeira
            codigo = None
            if isinstance(cad, Cadeira):
                codigo = getattr(cad, "codigo", None) or getattr(cad, "nome_cadeira", None) or getattr(cad, "nome", None)
            elif isinstance(cad, dict):
                codigo = cad.get("codigo") or cad.get("nome_cadeira") or cad.get("nome")

            if str(codigo) == str(codigo_cadeira):
                # atualiza as notas
                if isinstance(cad, Cadeira):
                    if isinstance(notas, Nota):
                        cad.notas = notas
                    elif isinstance(notas, dict):
                        cad.notas = Nota(
                            notas.get("va1"),
                            notas.get("va2"),
                            notas.get("va3"),
                            notas.get("recuperacao"),
                        )
                    else:
                        try:
                            cad.notas = Nota(notas[0], notas[1], notas[2], notas[3])  # type: ignore
                        except Exception:
                            pass
                else:
                    # cadeiras como dict
                    if isinstance(notas, Nota) and hasattr(notas, "to_dict"):
                        cad["notas"] = notas.to_dict()
                    else:
                        cad["notas"] = notas
                encontrado = True
                break

        if not encontrado:
            return False
        try:
            if isinstance(usuario, Usuario):
                self.repositorio.salvar_usuario(usuario)
            else:
                usuario["cadeiras"] = [
                    c.to_dict() if isinstance(c, Cadeira) and hasattr(c, "to_dict") else c
                    for c in cadeiras
                ]
                self.repositorio.salvar_usuario(usuario)
            return True
        except Exception:
            return False