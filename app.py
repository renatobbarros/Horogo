import os

from HOROGO.interface.interface_console import InterfaceConsole
from HOROGO.repository.repositorio_usuario import repositorio_usuario
from HOROGO.services.servico_auth import servico_auth
from HOROGO.services.servico_academico import servico_academico
from HOROGO.interface.interface_auth import InterfaceAutenticacao
from HOROGO.interface.interface_academica import InterfaceAcademica
from HOROGO.interface.interface_menu import InterfaceMenu

try:
    from HOROGO.interface.interface_horobot import InterfaceHorobot
except Exception:
    InterfaceHorobot = None


class AplicacaoHorogo:
    '''coordena a aplicação'''
    def __init__(self, console, horobot, auth, menu, serv_acad=None, interface_academica=None):
        self.console = console
        self.horobot = horobot
        self.auth = auth
        self.menu = menu
        self.serv_acad = serv_acad
        self.interface_academica = interface_academica

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

        # loop resiliente do menu principal: em caso de erro interno, volta ao dashboard
        while True:
            try:
                if hasattr(self.menu, "executar"):
                    # se a implementação do menu fornece um método executar, chamamos e se ele retornar, consideramos que o usuário saiu do menu
                    try:
                        self.menu.executar(usuario)
                    except Exception as e:
                        # não deixa a aplicação morrer por causa de um erro no menu
                        try:
                            self.console.exibir_erro(f"Erro no menu: {e}")
                            try:
                                self.console.pausar()
                            except Exception:
                                pass
                        except Exception:
                            pass
                        # volta a mostrar o dashboard
                        continue
                    # se executar retornou sem levantar, interrompe o loop
                    break
                opcoes = ["Notas", "Cadeiras", "Perfil", "Mural", "Calendário", "Atualizar Conta", "Sair"]
                try:
                    self.menu.mostrar_dashboard(usuario, opcoes)
                    escolha = self.menu.selecionar_opcao(len(opcoes))
                except Exception as e:
                    try:
                        self.console.exibir_erro(f"Erro ao mostrar opções do menu: {e}")
                        try:
                            self.console.pausar()
                        except Exception:
                            pass
                    except Exception:
                        pass
                    continue

                try:
                    # Notas
                    if escolha == 0:
                        if self.interface_academica:
                            # submenu de notas
                            while True:
                                try:
                                    self.console.exibir_mensagem("1 - Ver situação\n2 - Adicionar/Atualizar notas\n0 - Voltar", delay_segundos=0)
                                    if hasattr(self.console, 'obter_entrada'):
                                        opt_txt = self.console.obter_entrada("Escolha:")
                                    elif hasattr(self.console, 'obter_input'):
                                        opt_txt = self.console.obter_input("Escolha:")
                                    else:
                                        opt_txt = input("Escolha: ")
                                    try:
                                        opt = int(opt_txt)
                                    except Exception:
                                        self.console.exibir_mensagem("Opção inválida.")
                                        continue

                                    if opt == 1:
                                        try:
                                            self.interface_academica.executar_situacao_cadeiras(usuario)
                                        except Exception as e:
                                            try:
                                                self.console.exibir_erro(f"Erro ao exibir situação: {e}")
                                                try:
                                                    self.console.pausar()
                                                except Exception:
                                                    pass
                                            except Exception:
                                                pass
                                        try:
                                            self.console.pausar()
                                        except Exception:
                                            pass
                                    elif opt == 2:
                                        try:
                                            self.interface_academica.executar_menu_cadastrar_notas(usuario)
                                        except Exception as e:
                                            try:
                                                self.console.exibir_erro(f"Erro ao cadastrar notas: {e}")
                                                try:
                                                    self.console.pausar()
                                                except Exception:
                                                    pass
                                            except Exception:
                                                pass
                                        try:
                                            self.console.pausar()
                                        except Exception:
                                            pass
                                    elif opt == 0:
                                        break
                                    else:
                                        self.console.exibir_mensagem("Opção inválida.")
                                        continue
                                except Exception:
                                    # em caso de erro inesperado, volta ao dashboard
                                    try:
                                        self.console.exibir_erro("Erro no submenu de notas. Voltando ao menu principal.")
                                        try:
                                            self.console.pausar()
                                        except Exception:
                                            pass
                                    except Exception:
                                        pass
                                    break
                        else:
                            # comportamento anterior: listar notas simples
                            if hasattr(usuario, "obter_cadeiras"):
                                cadeiras = usuario.obter_cadeiras()
                            elif isinstance(usuario, dict):
                                cadeiras = usuario.get("cadeiras", [])
                            else:
                                cadeiras = []

                            if not cadeiras:
                                self.console.exibir_mensagem("Nenhuma cadeira encontrada.")
                            else:
                                for c in cadeiras:
                                    # c pode ser objeto Cadeira ou dicionario
                                    if hasattr(c, "get_notas_formatadas"):
                                        nome = getattr(c, "nome_cadeira", getattr(c, "nome", ""))
                                        self.console.exibir_mensagem(f"Cadeira: {nome}")
                                        self.console.exibir_mensagem(c.get_notas_formatadas())
                                    elif isinstance(c, dict):
                                        nome = c.get("nome_cadeira") or c.get("nome") or "Sem nome"
                                        self.console.exibir_mensagem(f"Cadeira: {nome}")
                                        notas = c.get("notas")
                                        if notas:
                                            try:
                                                from HOROGO.models.nota import Nota
                                                n = Nota.from_dict(notas) if hasattr(Nota, "from_dict") else None
                                                if n:
                                                    self.console.exibir_mensagem(n.to_dict().__str__())
                                                else:
                                                    self.console.exibir_mensagem(str(notas))
                                            except Exception:
                                                self.console.exibir_mensagem(str(notas))
                                        else:
                                            self.console.exibir_mensagem("Sem notas.")
                            self.console.pausar()
                    # Cadeiras
                    elif escolha == 1:
                        if self.interface_academica:
                            # submenu de cadeiras
                            while True:
                                try:
                                    self.console.exibir_mensagem("1 - Listar cadeiras\n2 - Cadastrar nova cadeira\n0 - Voltar", delay_segundos=0)
                                    if hasattr(self.console, 'obter_entrada'):
                                        opt_txt = self.console.obter_entrada("Escolha:")
                                    elif hasattr(self.console, 'obter_input'):
                                        opt_txt = self.console.obter_input("Escolha:")
                                    else:
                                        opt_txt = input("Escolha: ")
                                    try:
                                        opt = int(opt_txt)
                                    except Exception:
                                        self.console.exibir_mensagem("Opção inválida.")
                                        continue

                                    if opt == 1:
                                        # listar
                                        if hasattr(usuario, "obter_cadeiras"):
                                            cadeiras = usuario.obter_cadeiras()
                                        elif isinstance(usuario, dict):
                                            cadeiras = usuario.get("cadeiras", [])
                                        else:
                                            cadeiras = []
                                        self.interface_academica.listar_cadeiras_duas_colunas(cadeiras)
                                        self.console.pausar()
                                    elif opt == 2:
                                        # cadastrar
                                        try:
                                            self.interface_academica.executar_menu_cadastrar_cadeira(usuario)
                                        except Exception as e:
                                            try:
                                                self.console.exibir_erro(f"Erro ao cadastrar cadeira: {e}")
                                                try:
                                                    self.console.pausar()
                                                except Exception:
                                                    pass
                                            except Exception:
                                                pass
                                        self.console.pausar()
                                    elif opt == 0:
                                        break
                                    else:
                                        self.console.exibir_mensagem("Opção inválida.")
                                        continue
                                except Exception:
                                    try:
                                        self.console.exibir_erro("Erro no submenu de cadeiras. Voltando ao menu principal.")
                                        try:
                                            self.console.pausar()
                                        except Exception:
                                            pass
                                    except Exception:
                                        pass
                                    break
                        else:
                            self.console.exibir_mensagem("Interface de cadeiras não configurada.")
                        self.console.pausar()
                    elif escolha in (2, 3, 4, 5):
                        self.console.exibir_mensagem("Funcionalidade não implementada ainda.")
                        self.console.pausar()
                    elif escolha == 6:
                        self.console.exibir_mensagem("Saindo...")
                        break
                except Exception as e:
                    try:
                        self.console.exibir_erro(f"Erro ao executar ação do menu: {e}")
                        try:
                            self.console.pausar()
                        except Exception:
                            pass
                    except Exception:
                        pass
                    continue

            except Exception as e:
                try:
                    self.console.exibir_erro(f"Erro ao executar menu: {e}")
                    try:
                        self.console.pausar()
                    except Exception:
                        pass
                except Exception:
                    pass
                continue

        if self.horobot:
            try:
                self.horobot.exibir_dormindo()
            except Exception:
                pass


def main():
    '''montar as peças'''
    console = InterfaceConsole()
    horobot = InterfaceHorobot(console) if InterfaceHorobot else None

    # caminho simples para arquivo de dados, onde ele e criado em uma nova pasta chamada dados/conta.json
    repo_file = os.path.join(os.path.dirname(__file__), "HOROGO", "models", "Dados", "conta.json")
    repo = repositorio_usuario(repo_file)

    serv_auth = servico_auth(repo)
    serv_acad = servico_academico(repo)

    interface_auth = InterfaceAutenticacao(serv_auth, console, horobot)
    interface_academica = InterfaceAcademica(console, horobot, serv_acad)
    menu_principal = InterfaceMenu(console)

    # passa serv_acad e interface_academica para o orquestrador
    app = AplicacaoHorogo(console, horobot, interface_auth, menu_principal, serv_acad=serv_acad, interface_academica=interface_academica)
    app.run()


if __name__ == "__main__":
    main()