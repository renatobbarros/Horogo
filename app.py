import json
import os
from typing import Any, List, Optional, Dict
from pathlib import Path

from HOROGO.interface.interface_console import InterfaceConsole
from HOROGO.interface.interface_menu import InterfaceMenu
from HOROGO.interface.interface_auth import InterfaceAutenticacao
from HOROGO.interface.interface_academica import InterfaceAcademica
from HOROGO.interface.interface_mural import InterfaceMural
from HOROGO.interface.interface_perfil import InterfacePerfil
from HOROGO.interface.interface_horobot import InterfaceHorobot

from HOROGO.repository.repositorio_usuario import repositorio_usuario
from HOROGO.repository.repositorio_evento import RepositorioEvento

from HOROGO.services.servico_auth import servico_auth
from HOROGO.services.servico_academico import servico_academico
from HOROGO.services.servico_mural import ServicoMural
from HOROGO.services.servico_perfil import ServicoPerfil
from HOROGO.services.servico_xp import ServicoXP


class repositorio_usuario:
    """Repositório para usuários, armazenados em JSON."""

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

        if isinstance(usuario, dict):
            usuario_obj = Usuario.from_dict(usuario)
        elif isinstance(usuario, Usuario):
            usuario_obj = usuario
        else:
            raise TypeError("salvar_usuario espera dict ou Usuario")

        existente = self.encontrar_usuario(usuario_obj.usuario)
        if existente:
            for i, u in enumerate(self.usuarios):
                if (isinstance(u, Usuario) and u.usuario == existente.usuario) or (isinstance(u, dict) and (u.get("usuario") == existente.usuario or u.get("nome") == existente.usuario)):
                    self.usuarios[i] = usuario_obj
                    break
        else:
            self.usuarios.append(usuario_obj)

        self._salvar_json()


class Usuario:
    def __init__(
        self,
        usuario: str,
        senha: str,
        instituicao: str,
        periodo: Any,
        xp: int = 0,
        nivel: int = 1,
        cadeiras: Optional[List[Any]] = None,
    ):
        self.usuario = usuario
        self.senha = senha
        self.instituicao = instituicao
        self.periodo = periodo
        self.xp = int(xp) if xp is not None else 0
        self.nivel = int(nivel) if nivel is not None else 1
        self.cadeiras = cadeiras if cadeiras is not None else []

    def verificar_senha(self, senha_input: Optional[str]) -> bool:
        if senha_input is None:
            return False
        return self.senha == senha_input.strip()

    def adicionar_cadeira(self, cadeira_obj: Any) -> None:
        if cadeira_obj is None:
            return
        if isinstance(cadeira_obj, dict):
            try:
                cadeira_obj = Cadeira.from_dict(cadeira_obj)
            except Exception:
                self.cadeiras.append(cadeira_obj)
                return
        if isinstance(cadeira_obj, Cadeira):
            self.cadeiras.append(cadeira_obj)
        else:
            self.cadeiras.append(cadeira_obj)

    def obter_cadeiras(self) -> List[Any]:
        return self.cadeiras

    def to_dict(self) -> Dict[str, Any]:
        cadeiras_serial = []
        for c in self.cadeiras:
            if hasattr(c, "to_dict"):
                cadeiras_serial.append(c.to_dict())
            else:
                cadeiras_serial.append(c)
        return {
            "usuario": self.usuario,
            "nome": self.usuario,
            "senha": self.senha,
            "instituicao": self.instituicao,
            "periodo": self.periodo,
            "xp": self.xp,
            "nivel": self.nivel,
            "cadeiras": cadeiras_serial,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        if data is None:
            raise ValueError("data não pode ser None")
        usuario = data.get("usuario") or data.get("nome") or ""
        senha = data.get("senha") or ""
        instituicao = data.get("instituicao")
        periodo = data.get("periodo")
        xp = data.get("xp", 0)
        nivel = data.get("nivel", 1)

        cadeiras_data = data.get("cadeiras") or []
        cadeiras = []
        for c in cadeiras_data:
            if isinstance(c, dict):
                try:
                    cadeiras.append(Cadeira.from_dict(c))
                except Exception:
                    cadeiras.append(c)
            else:
                cadeiras.append(c)

        return cls(usuario, senha, instituicao, periodo, xp=xp, nivel=nivel, cadeiras=cadeiras)


class AplicacaoHorogo:
    def __init__(self):
        base_dir = Path(__file__).resolve().parent
        dados_dir = base_dir / "HOROGO" / "models" / "Dados"
        dados_dir.mkdir(parents=True, exist_ok=True)

        self.repo_usuarios = repositorio_usuario(str(dados_dir / "conta.json"))
        self.repo_eventos = RepositorioEvento(str(dados_dir / "eventos.json"))

        self.sv_auth = servico_auth(self.repo_usuarios)
        self.sv_acad = servico_academico(self.repo_usuarios)
        self.sv_mural = ServicoMural(self.repo_eventos, self.repo_usuarios)
        self.sv_perfil = ServicoPerfil(self.repo_usuarios)
        self.sv_xp = ServicoXP(self.repo_usuarios)

        self.console = InterfaceConsole()
        self.horobot = InterfaceHorobot(self.console)

        self.ui_auth = InterfaceAutenticacao(self.sv_auth, self.console, self.horobot)
        self.ui_menu = InterfaceMenu(self.console, xp_bar_width=30)
        self.ui_acad = InterfaceAcademica(self.console, self.sv_acad, col_width=34)
        self.ui_mural = InterfaceMural(self.console, self.sv_mural)
        self.ui_perfil = InterfacePerfil(self.console, self.sv_perfil)

        self.usuario = None

    def _dar_xp(self, acao: str, quantidade=None):
        if not self.usuario:
            return
        nome = getattr(self.usuario, "usuario", None) or getattr(self.usuario, "nome", None)
        ok, msg, info = self.sv_xp.adicionar_xp(nome, acao, quantidade)
        if ok:
            try:
                self.console.exibir_sucesso(msg)
            except Exception:
                print(f"\n  ✓ {msg}")
            if info.get("subiu_nivel"):
                try:
                    self.horobot.exibir_celebracao()
                except Exception:
                    pass

    def _menu_academico(self):
        while True:
            self.console.limpar_tela()
            self.console.exibir_titulo("Área Acadêmica")
            print("  [1] Ver situação das cadeiras")
            print("  [2] Cadastrar nova cadeira")
            print("  [3] Cadastrar/Atualizar notas")
            print("  [0] Voltar\n")
            op = input("  » ").strip()
            if op == "0":
                return
            if op == "1":
                self.ui_acad.executar_situacao_cadeiras(self.usuario)
                self.console.pausar()
            elif op == "2":
                if self.ui_acad.executar_menu_cadastrar_cadeira(self.usuario):
                    self._dar_xp("cadastrar_cadeira")
                self.console.pausar()
            elif op == "3":
                self.ui_acad.executar_menu_cadastrar_notas(self.usuario)
                self.console.pausar()
            else:
                self.console.exibir_erro("Opção inválida")

    def run(self):
        self.console.limpar_tela()
        self.horobot.exibir_apresentacao()
        print("\n  Bem-vindo ao HOROGO!")
        print("  Seu assistente pessoal para gerenciar sua vida acadêmica.\n")
        self.console.pausar()

        self.usuario = self.ui_auth.executar_login()
        if not self.usuario:
            return
        self._dar_xp("login_diario")

        while True:
            opcoes = ["Área Acadêmica", "Mural de Eventos", "Perfil", "Sair"]
            self.ui_menu.mostrar_dashboard(self.usuario, opcoes, servico_xp=self.sv_xp)
            idx = self.ui_menu.selecionar_opcao(len(opcoes))
            if idx == 0:
                self._menu_academico()
            elif idx == 1:
                self.ui_mural.executar_menu_mural(self.usuario)
            elif idx == 2:
                self.ui_perfil.executar(self.usuario)
            elif idx == 3:
                try:
                    self.horobot.exibir_dormindo()
                except Exception:
                    pass
                print("\n  Até a próxima!")
                break


def main():
    app = AplicacaoHorogo()
    app.run()


if __name__ == "__main__":
    main()