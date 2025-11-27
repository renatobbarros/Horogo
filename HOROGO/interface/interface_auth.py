from typing import Optional
from ..models.usuario import Usuario
from ..services.servico_auth import ServicoAuth
from .interface_console import InterfaceConsole
from .interface_horobot import InterfaceHorobot


class InterfaceAutenticacao:
	"""Interface de autenticação via console e opcionalmente o HOROBOT."""
	def __init__(self, servico_auth: ServicoAuth, console: InterfaceConsole, horobot: Optional[InterfaceHorobot] = None):
		self.servico = servico_auth
		self.console = console
		self.horobot = horobot

	def executar_login(self) -> Optional[Usuario]:
		"""Loop de login: pede credenciais, chama o serviço e trata falhas."""
		while True:
			self.console.limpar_tela()
			self.console.exibir_mensagem("LOGIN", delay_segundos=0)
			nome = self.console.obter_input("Digite seu nome de usuário:")
			senha = self.console.obter_senha("Digite sua senha:")

			usuario_obj = self.servico.login(nome, senha)
			if usuario_obj:
				self.console.exibir_mensagem("Login efetuado com sucesso!", delay_segundos=1)
				return usuario_obj

			# Falha de login: mostrar menu de opções
			self.console.exibir_mensagem("Usuário ou senha incorretos.", delay_segundos=0)
			acao = self._exibir_menu_login_falho()
			if acao == "TENTAR_NOVAMENTE":
				continue
			if acao == "CADASTRO":
				resultado = self.executar_cadastro()
				if isinstance(resultado, Usuario):
					return resultado
				continue
			if acao == "SAIR":
				return None

	def executar_cadastro(self) -> Optional[Usuario]:
		"""Loop de cadastro: coleta dados, chama serviço e exibe mensagens de erro/ sucesso."""
		while True:
			self.console.limpar_tela()
			self.console.exibir_mensagem("CADASTRO", delay_segundos=0)
			nome = self.console.obter_input("Escolha um nome de usuário (até 20 caracteres):")
			senha = self.console.obter_senha("Escolha uma senha (até 12 caracteres):")
			senha_conf = self.console.obter_senha("Confirme a senha:")
			if senha != senha_conf:
				self.console.exibir_mensagem("As senhas não conferem. Tente novamente.", delay_segundos=1)
				continue

			instituicao = self.console.obter_input("Instituição:")
			periodo = self.console.obter_input("Período (número):")

			resultado = self.servico.registrar_usuario(nome, senha, instituicao, periodo)
			if isinstance(resultado, Usuario):
				self.console.exibir_mensagem("Conta criada com sucesso!", delay_segundos=1)
				return resultado
			else:
				# resultado é string com mensagem de erro
				self.console.exibir_mensagem(resultado, delay_segundos=1)
				# loop continua para o usuário corrigir

	def _exibir_menu_login_falho(self) -> str:
		"""Menu mostrado após tentativa de login falha. Retorna ação string."""
		while True:
			self.console.exibir_mensagem("Escolha uma opção:", delay_segundos=0)
			self.console.exibir_mensagem("1 - Tentar novamente\n2 - Criar conta\n0 - Cancelar", delay_segundos=0)
			escolha = self.console.obter_input("Digite a opção (número):")
			try:
				op = int(escolha)
			except ValueError:
				self.console.exibir_mensagem("Digite apenas números.", delay_segundos=0)
				continue

			if op == 1:
				return "TENTAR_NOVAMENTE"
			if op == 2:
				return "CADASTRO"
			if op == 0:
				return "SAIR"
			self.console.exibir_mensagem("Opção inválida.", delay_segundos=0)

