import os

from HOROGO.interface.interface_console import InterfaceConsole
from HOROGO.repository.repositorio_usuario import repositorio_usuario
from HOROGO.services.servico_auth import servico_auth
from HOROGO.services.servico_academico import servico_academico
from HOROGO.interface.interface_auth import InterfaceAutenticacao
from HOROGO.interface.interface_academica import InterfaceAcademica
from HOROGO.interface.interface_menu import InterfaceMenu

# tentar importar o horobot, mas não morrer se não existir
try:
    from HOROGO.interface.interface_horobot import InterfaceHorobot
except Exception:
    InterfaceHorobot = None


class AplicacaoHorogo:
    '''coordena a aplicação'''
    def __init__(self, console, horobot, auth, menu):
        self.console = console
        self.horobot = horobot
        self.auth = auth
        self.menu = menu

    def _iniciar_autenticacao(self):
        '''verifica se o usuário quer logar ou cadastrar'''
        while True:
            prompt = "Antes de mais nada, você já possui cadastro no HOROGO?\n1 - Sim\n2 - Não"
            escolha_txt = self.console.obter_entrada(prompt)
            try:
                escolha = int(escolha_txt)
            except Exception:
                self.console.exibir_mensagem("Por favor digite 1 ou 2.")
                continue

            if escolha == 1:
                return self.auth.executar_login()
            if escolha == 2:
                return self.auth.executar_cadastro()
            self.console.exibir_mensagem("Opção inválida. Tente novamente.")

    def run(self):
        # apresentação
        if self.horobot:
            try:
                self.horobot.exibir_apresentacao()
            except Exception:
                pass

        self.console.exibir_mensagem("Bem vindo ao HOROGO!")
        self.console.exibir_mensagem("Vou te ajudar a gerenciar suas cadeiras e notas.")

        usuario = self._iniciar_autenticacao()
        if not usuario:
            self.console.exibir_mensagem("Nenhum usuário autenticado. Encerrando.")
            if self.horobot:
                try:
                    self.horobot.exibir_dormindo()
                except Exception:
                    pass
            return

        # tenta usar o menu principal (se tiver sido implementado)
        try:
            if hasattr(self.menu, "executar"):
                self.menu.executar(usuario)
            else:
                # fallback simples: mostrar dashboard e esperar escolha
                opcoes = ["Ver cadeiras", "Sair"]
                self.menu.mostrar_dashboard(usuario, opcoes)
                escolha = self.menu.selecionar_opcao(len(opcoes))
                if escolha == 0:
                    self.console.exibir_mensagem("Funcionalidade 'Ver cadeiras' ainda não implementada.")
        except Exception as e:
            # mensagem simples de erro
            self.console.exibir_erro(f"Erro ao executar menu: {e}")

        if self.horobot:
            try:
                self.horobot.exibir_dormindo()
            except Exception:
                pass


def main():
    '''montar as peças'''
    console = InterfaceConsole()
    horobot = InterfaceHorobot(console) if InterfaceHorobot else None

    # caminho simples para arquivo de dados (mesmo diretório do app.py)
    repo_file = os.path.join(os.path.dirname(__file__), "conta.json")
    repo = repositorio_usuario(repo_file)

    serv_auth = servico_auth(repo)
    serv_acad = servico_academico(repo)

    interface_auth = InterfaceAutenticacao(serv_auth, console, horobot)
    interface_academica = InterfaceAcademica(console)
    menu_principal = InterfaceMenu(console)

    app = AplicacaoHorogo(console, horobot, interface_auth, menu_principal)
    app.run()


if __name__ == "__main__":
    main()