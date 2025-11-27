from HOROGO.interface.interface_console import InterfaceConsole
from HOROGO.interface.interface_horobot import InterfaceHorobot
from HOROGO.repository.repositorio_usuario import repositorio_usuario
from HOROGO.services.servico_auth import servico_auth
from HOROGO.services.servico_academico import servico_academico
from HOROGO.interface.interface_auth import InterfaceAutenticacao
from HOROGO.interface.interface_academica import InterfaceAcademica
from HOROGO.interface.interface_menu import InterfaceMenu


class AplicacaoHorogo:
    """Classe principal que orquestra a aplicação HOROGO."""
    def __init__(self, console: InterfaceConsole, horobot: InterfaceHorobot,
                 interface_auth: InterfaceAutenticacao, menu_principal: InterfaceMenu):
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
                escolha = int(self.console.obter_entrada(prompt))
                self.console.limpar_tela()
                if escolha == 1:
                    return self.interface_auth.executar_login()
                if escolha == 2:
                    return self.interface_auth.executar_cadastro()
                self.console.exibir_mensagem("Opção inválida. Tente novamente.")
            except ValueError:
                self.console.exibir_mensagem("Digite apenas números.")

    def run(self):
        """Fluxo principal da aplicação."""
        try:
            self.horobot.exibir_apresentacao()
        except Exception:
            pass

        self.console.exibir_mensagem("É um prazer te receber aqui!")
        self.console.exibir_mensagem("Serei seu amigo e guia durante sua jornada acadêmica!")

        usuario = self._iniciar_autenticacao()
        if usuario:
            # Tenta executar método 'executar' do menu; se não existir, usa fallback simples
            try:
                self.menu_principal.executar(usuario)
            except AttributeError:
                try:
                    # fallback: mostrar dashboard simples e aguardar seleção
                    opcoes = ["Ver cadeiras", "Sair"]
                    self.menu_principal.mostrar_dashboard(usuario, opcoes)
                    escolha = self.menu_principal.selecionar_opcao(len(opcoes))
                    if escolha == 0:
                        self.console.exibir_mensagem("Funcionalidade 'Ver cadeiras' não implementada.")
                except Exception as e:
                    self.console.exibir_mensagem(f"Erro ao executar o menu principal: {e}")

        try:
            self.horobot.exibir_dormindo()
        except Exception:
            pass


def main():
    # CAMADA 1: I/O (Console) 
    console = InterfaceConsole()
    horobot = InterfaceHorobot(console)

    # CAMADA 2: DADOS (Repositório) 
    repo_usuario = repositorio_usuario("conta.json")

    # CAMADA 3: LÓGICA (Serviços) 
    serv_auth = servico_auth(repo_usuario)
    serv_acad = servico_academico(repo_usuario)

    # CAMADA 4: INTERFACE (Views) 
    interface_auth = InterfaceAutenticacao(serv_auth, console, horobot)
    interface_academica = InterfaceAcademica(console)
    menu_principal = InterfaceMenu(console)

    # CAMADA 5: APLICAÇÃO (Orquestrador)
    app = AplicacaoHorogo(console, horobot, interface_auth, menu_principal)
    app.run()


if __name__ == "__main__":
    main()