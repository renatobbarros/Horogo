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
from HOROGO.services.servico_calendario import servico_calendario

from HOROGO.interface.interface_calendario import InterfaceCalendario


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
        self.sv_cal = servico_calendario(str(dados_dir / "eventos.json"))

        self.console = InterfaceConsole()
        self.horobot = InterfaceHorobot(self.console)

        self.ui_auth = InterfaceAutenticacao(self.sv_auth, self.console, self.horobot)
        self.ui_menu = InterfaceMenu(self.console, xp_bar_width=30)
        self.ui_acad = InterfaceAcademica(self.console, self.sv_acad, col_width=34)
        self.ui_mural = InterfaceMural(self.console, self.sv_mural)
        self.ui_perfil = InterfacePerfil(self.console, self.sv_perfil)
        self.ui_calendario = InterfaceCalendario(self.sv_cal, self.console, self.repo_usuarios)

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

        while True:
            self.console.limpar_tela()
            self.console.exibir_titulo("BEM-VINDO")
            print("  [1] Fazer Login")
            print("  [2] Criar Conta")
            print("  [0] Sair\n")
            escolha = input("  » ").strip()
            
            if escolha == "1":
                self.usuario = self.ui_auth.executar_login()
                if self.usuario:
                    self._dar_xp("login_diario")
                    break
            elif escolha == "2":
                self.usuario = self.ui_auth.executar_cadastro()
                if self.usuario:
                    self._dar_xp("login_diario")
                    break
            elif escolha == "0":
                return
            else:
                self.console.exibir_erro("Opção inválida. Digite 1, 2 ou 0.")
                self.console.pausar()
        
        if not self.usuario:
            return

        while True:
            opcoes = ["Área Acadêmica", "Calendário", "Mural de Eventos", "Perfil", "Sair"]
            self.ui_menu.mostrar_dashboard(self.usuario, opcoes, servico_xp=self.sv_xp, servico_cal=self.sv_cal)
            idx = self.ui_menu.selecionar_opcao(len(opcoes))
            if idx == 0:
                self._menu_academico()
            elif idx == 1:
                self.ui_calendario.executar(self.usuario)
            elif idx == 2:
                self.ui_mural.executar_menu_mural(self.usuario)
            elif idx == 3:
                self.ui_perfil.executar(self.usuario)
            elif idx == 4:
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