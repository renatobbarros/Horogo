from HOROGO.interface.interface_console import InterfaceConsole
from HOROGO.interface.interface_horobot import InterfaceHorobot
from HOROGO.repository.repositorio_usuario import RepositorioUsuario
from HOROGO.services.servico_auth import ServicoAuth
from HOROGO.services.servico_academico import ServicoAcademico
from HOROGO.interface.interface_auth import InterfaceAutenticacao
from HOROGO.interface.interface_academica import InterfaceAcademica
from HOROGO.interface.interface_menu import InterfaceMenuPrincipal


class AplicacaoHorogo:
    """Classe principal que orquestra a aplicação HOROGO."""
    def __init__(self, console: InterfaceConsole, horobot: InterfaceHorobot,
                 interface_auth: InterfaceAutenticacao, menu_principal: InterfaceMenuPrincipal):
        self.console = console
        self.horobot = horobot
        self.interface_auth = interface_auth
        self.menu_principal = menu_principal

    def _iniciar_autenticacao(self):
        """Pergunta se o usuário já tem cadastro e inicia o fluxo de login/cadastro."""
        while True:
            try:
                prompt = ("Antes de mais nada, você já possui cadastro no HOROGO?\n"
                          "1 - Sim\n2 - Não")
                escolha = int(self.console.obter_input(prompt))
                self.console.limpar_tela()
                if escolha == 1:
                    return self.interface_auth.executar_login()
                if escolha == 2:
                    return self.interface_auth.executar_cadastro()
                self.console.exibir_mensagem("Opção inválida. Tente novamente.", delay_segundos=1)
            except ValueError:
                self.console.exibir_mensagem("Digite apenas números.", delay_segundos=1)

    def run(self):
        """Fluxo principal da aplicação."""
        try:
            self.horobot.exibir_apresentacao()
        except Exception:
            # Se horobot não estiver completo, apenas continue
            pass

        self.console.exibir_mensagem("É um prazer te receber aqui!", delay_segundos=1)
        self.console.exibir_mensagem("Serei seu amigo e guia durante sua jornada acadêmica!", delay_segundos=1)

        usuario = self._iniciar_autenticacao()
        if usuario:
            try:
                self.menu_principal.executar(usuario)
            except Exception as e:
                # Erro de runtime no menu: exiba mensagem e finalize graciosamente
                self.console.exibir_mensagem(f"Erro ao executar o menu principal: {e}", delay_segundos=2)

        try:
            self.horobot.exibir_dormindo()
        except Exception:
            pass


def main():
    # CAMADA 1: I/O (Console) 
    console = InterfaceConsole()
    horobot = InterfaceHorobot(console)

    # CAMADA 2: DADOS (Repositório) 
    repo_usuario = RepositorioUsuario("conta.json")

    # CAMADA 3: LÓGICA (Serviços) 
    servico_auth = ServicoAuth(repo_usuario)
    servico_academico = ServicoAcademico(repo_usuario)

    # CAMADA 4: INTERFACE (Views) 
    interface_auth = InterfaceAutenticacao(servico_auth, console, horobot)
    interface_academica = InterfaceAcademica(console, horobot, servico_academico)
    menu_principal = InterfaceMenuPrincipal(console, horobot, repo_usuario, interface_academica)

    # CAMADA 5: APLICAÇÃO (Orquestrador)
    app = AplicacaoHorogo(console, horobot, interface_auth, menu_principal)
    app.run()


if __name__ == "__main__":
    main()
