from typing import Optional, Any
from .interface_console import InterfaceConsole
from .interface_horobot import InterfaceHorobot


class InterfaceAutenticacao:
    def __init__(self, servico_auth: Any, console: InterfaceConsole, horobot: Optional[InterfaceHorobot] = None):
        self.servico = servico_auth
        self.console = console
        self.horobot = horobot

    def executar_login(self) -> Optional[Any]:
        """Loop de login: pede credenciais, chama o serviço e trata falhas."""
        while True:
            try:
                self.console.limpar_tela()
            except Exception:
                pass

            if hasattr(self.console, "exibir_titulo"):
                try:
                    self.console.exibir_titulo("LOGIN")
                except Exception:
                    pass

            nome = self.console.obter_entrada("Digite seu nome de usuário")
            senha = self.console.obter_entrada("Digite sua senha")

            try:
                usuario_obj = self.servico.login(nome, senha)
            except Exception as e:
                self.console.exibir_erro(str(e) if hasattr(self.console, "exibir_erro") else f"Erro: {e}")
                try:
                    self.console.pausar()
                except Exception:
                    pass
                usuario_obj = None

            if usuario_obj:
                if hasattr(self.console, "exibir_sucesso"):
                    self.console.exibir_sucesso("Login efetuado com sucesso!")
                else:
                    self.console.exibir_mensagem("Login efetuado com sucesso!")
                return usuario_obj

            # se chegou aqui, falhou
            if hasattr(self.console, "exibir_erro"):
                self.console.exibir_erro("Usuário ou senha incorretos.")
                try:
                    self.console.pausar()
                except Exception:
                    pass
            else:
                self.console.exibir_mensagem("Usuário ou senha incorretos.")

            # menu simples após falha
            while True:
                escolha = self.console.obter_entrada("1-Tentar novamente  2-Criar conta  0-Sair")
                if escolha in ("1", "1 "):
                    break  # volta ao início do loop externo para tentar login
                if escolha == "2":
                    resultado = self.executar_cadastro()
                    if resultado:
                        return resultado
                    break  # depois do cadastro falho/sem retorno, volta ao menu de login
                if escolha == "0":
                    return None
                self.console.exibir_mensagem("Opção inválida. Digite 1, 2 ou 0.")

    def executar_cadastro(self) -> Optional[Any]:
        """Loop de cadastro: coleta dados, chama serviço e exibe mensagens de erro/ sucesso."""
        while True:
            try:
                self.console.limpar_tela()
            except Exception:
                pass

            if hasattr(self.console, "exibir_titulo"):
                try:
                    self.console.exibir_titulo("CADASTRO")
                except Exception:
                    pass

            nome = self.console.obter_entrada("Escolha um nome de usuário (até 20 caracteres)")
            senha = self.console.obter_entrada("Escolha uma senha (até 12 caracteres)")
            senha_conf = self.console.obter_entrada("Confirme a senha")
            if senha != senha_conf:
                self.console.exibir_erro("As senhas não conferem. Tente novamente.")
                try:
                    self.console.pausar()
                except Exception:
                    pass
                continue

            instituicao = self.console.obter_entrada("Instituição")
            periodo = self.console.obter_entrada("Período (número)")

            try:
                resultado = self.servico.registrar_usuario(nome, senha, instituicao, periodo)
            except Exception as e:
                self.console.exibir_erro(f"Erro ao registrar: {e}")
                try:
                    self.console.pausar()
                except Exception:
                    pass
                continue

            # servico pode retornar string
            if isinstance(resultado, str):
                self.console.exibir_erro(resultado)
                try:
                    self.console.pausar()
                except Exception:
                    pass
                continue

            if resultado:
                try:
                    self.console.exibir_sucesso("Conta criada com sucesso!")
                except Exception:
                    self.console.exibir_mensagem("Conta criada com sucesso!")
                return resultado

            # caso inesperado, mostra erro genérico e repete
            self.console.exibir_erro("Falha ao criar conta. Tente novamente.")
            try:
                self.console.pausar()
            except Exception:
                pass

