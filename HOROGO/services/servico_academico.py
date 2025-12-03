from typing import Any, Union
from ..repository.repositorio_usuario import repositorio_usuario
from ..models.usuario import Usuario
from ..models.cadeira import Cadeira
from ..models.nota import Nota


class servico_academico:
    """mesma coisa do de autenticação, mas para coisas academicas. adicionar cadeira, atualizar notas, etc."""
    def __init__(self, repositorio: repositorio_usuario):
        self.repositorio = repositorio

    def criar_nova_cadeira(self, nome_cadeira: str, codigo_cadeira: str, periodo: Any) -> dict:
        """Cria um dicionário representando a cadeira com validações."""
        nome = str(nome_cadeira or "").strip()
        if not nome or len(nome) > 50:
            raise ValueError("Nome da cadeira inválido (1-50 caracteres)")

        periodo_str = str(periodo).strip()
        if not periodo_str.isdigit() or not (1 <= int(periodo_str) <= 15):
            raise ValueError("Período inválido (use número entre 1 e 15)")

        codigo = None if codigo_cadeira is None else str(codigo_cadeira)
        if codigo is not None and len(codigo) > 20:
            raise ValueError("Código da cadeira muito longo (máx 20 caracteres)")

        return {
            "nome": nome,
            "nome_cadeira": nome,
            "codigo": codigo,
            "periodo": int(periodo_str),
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
        """Atualiza as notas de uma cadeira do usuário."""
        usuario = self.repositorio.encontrar_usuario(nome_usuario)
        if not usuario:
            return False

        # pega lista de cadeiras (objetos ou dicionários)
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
                # atualiza as notas com validação (0-10)
                def _validar_valor(v):
                    if v is None:
                        return True
                    try:
                        f = float(v)
                    except Exception:
                        return False
                    return 0.0 <= f <= 10.0

                if isinstance(cad, Cadeira):
                    if isinstance(notas, Nota):
                        # valida atributos do objeto Nota
                        for attr in ("va1", "va2", "va3"):
                            val = getattr(notas, attr, None)
                            if val is not None and not _validar_valor(val):
                                return False
                        cad.notas = notas
                    elif isinstance(notas, dict):
                        va1 = notas.get("va1")
                        va2 = notas.get("va2")
                        va3 = notas.get("va3")
                        if not (_validar_valor(va1) and _validar_valor(va2) and _validar_valor(va3)):
                            return False
                        cad.notas = Nota(
                            None if va1 is None else float(va1),
                            None if va2 is None else float(va2),
                            None if va3 is None else float(va3),
                            notas.get("recuperacao"),
                        )
                    else:
                        # tenta iterável
                        try:
                            vals = list(notas)
                            va1 = vals[0] if len(vals) > 0 else None
                            va2 = vals[1] if len(vals) > 1 else None
                            va3 = vals[2] if len(vals) > 2 else None
                            if not (_validar_valor(va1) and _validar_valor(va2) and _validar_valor(va3)):
                                return False
                            cad.notas = Nota(
                                None if va1 is None else float(va1),
                                None if va2 is None else float(va2),
                                None if va3 is None else float(va3),
                            )
                        except Exception:
                            return False
                else:
                    # cadeiras como dicionarios
                    if isinstance(notas, Nota) and hasattr(notas, "to_dict"):
                        # valida por conversão
                        nd = notas.to_dict()
                        if not all(_validar_valor(nd.get(k)) for k in ("va1", "va2", "va3")):
                            return False
                        cad["notas"] = nd
                    elif isinstance(notas, dict):
                        if not (_validar_valor(notas.get("va1")) and _validar_valor(notas.get("va2")) and _validar_valor(notas.get("va3"))):
                            return False
                        cad["notas"] = {
                            "va1": None if notas.get("va1") is None else float(notas.get("va1")),
                            "va2": None if notas.get("va2") is None else float(notas.get("va2")),
                            "va3": None if notas.get("va3") is None else float(notas.get("va3")),
                            "recuperacao": notas.get("recuperacao"),
                        }
                    else:
                        # iterável
                        try:
                            vals = list(notas)
                            va1 = vals[0] if len(vals) > 0 else None
                            va2 = vals[1] if len(vals) > 1 else None
                            va3 = vals[2] if len(vals) > 2 else None
                            if not (_validar_valor(va1) and _validar_valor(va2) and _validar_valor(va3)):
                                return False
                            cad["notas"] = {
                                "va1": None if va1 is None else float(va1),
                                "va2": None if va2 is None else float(va2),
                                "va3": None if va3 is None else float(va3),
                            }
                        except Exception:
                            return False

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