from typing import Optional, Any
from .interface_console import InterfaceConsole
from .interface_horobot import InterfaceHorobot


class InterfaceAutenticacao:
    def __init__(self, servico_auth: Any, console: InterfaceConsole, horobot: Optional[InterfaceHorobot] = None):
        self.servico = servico_auth
        self.console = console
        self.horobot = horobot

    def executar_login(self) -> Optional[Any]:
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

            nome = self.console.obter_entrada("Digite seu nome de usuário [0 para voltar]")
            if nome == "0":
                return None
            
            senha = self.console.obter_entrada("Digite sua senha [0 para voltar]")
            if senha == "0":
                return None

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

            if hasattr(self.console, "exibir_erro"):
                self.console.exibir_erro("Usuário ou senha incorretos.")
                try:
                    self.console.pausar()
                except Exception:
                    pass
            else:
                self.console.exibir_mensagem("Usuário ou senha incorretos.")

            while True:
                escolha = self.console.obter_entrada("1-Tentar novamente  2-Criar conta  0-Sair")
                if escolha in ("1", "1 "):
                    break
                if escolha == "2":
                    resultado = self.executar_cadastro()
                    if resultado:
                        return resultado
                    break
                if escolha == "0":
                    return None
                self.console.exibir_mensagem("Opção inválida. Digite 1, 2 ou 0.")

    def executar_cadastro(self) -> Optional[Any]:
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

            nome = self.console.obter_entrada("Escolha um nome de usuário (até 20 caracteres) [0 para voltar]")
            if nome == "0":
                return None
            
            senha = self.console.obter_entrada("Escolha uma senha (até 12 caracteres) [0 para voltar]")
            if senha == "0":
                return None
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

            self.console.exibir_erro("Falha ao criar conta. Tente novamente.")
            try:
                self.console.pausar()
            except Exception:
                pass

