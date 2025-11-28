# ...existing code...
class InterfaceHorobot:

    def __init__(self, console=None):
        self.console = console

    def _print_art(self, art):
        if self.console and hasattr(self.console, "exibir_mensagem"):
            try:
                # usar exibir_mensagem para manter consistência com InterfaceConsole
                for line in art.splitlines():
                    self.console.exibir_mensagem(line)
                return
            except Exception:
                pass
        print(art)

    # métodos esperados pelo app
    def exibir_apresentacao(self):
        self._print_art(horobot_apresentacao)

    def exibir_celebracao(self):
        self._print_art(horobot_celebracao)

    def exibir_confuso(self):
        self._print_art(horobot_confuso)

    def exibir_pensando(self):
        self._print_art(horobot_pensando)

    def exibir_dormindo(self):
        self._print_art(horobot_dormindo)

horobot_apresentacao = r"""
          +-------------------------------------------------+
          |  Olá! Sou o Horobot, seu assistente de estudos. |
          +-------------------------------------------------+
                   \
                    \
              .------.
         o -- |  ^ ^   | -- o
              '------'
             / [ ** ] \
            /_________\
              | | | |
             '-----'
"""

horobot_celebracao = r"""
        +---------------------------------+
        |  UAU! VOCÊ SUBIU DE NÍVEL!      |
        |  Seu cérebro está evoluindo!    |
        +---------------------------------+
                 \
                  \
            ,    .--.    ,
             \'--: ^o^ :--'/
              '--.---.--'
              / [ ★★★ ] \
             /___________\
               | | | |
              '-----'
"""

horobot_confuso = r"""
        +---------------------------------+
        |  Hmm... Não reconheci esse      |
        |  comando. Tente de novo!        |
        +---------------------------------+
                 \
                  \
              .------.
         o -- | o_O ?  |
              '------'
             / [!!!] \
            /_________\
              | | | |
             '-----'
"""

horobot_pensando = r"""
        +---------------------------------+
        |  Processando e salvando seus    |
        |  dados... Um momento!           |
        +---------------------------------+
                 \
                  \
              .------.
         o -- | . . .  | -- o
              '------'
             / [ ~~~ ] \
            /_________\
              | | | |
             '-----'
"""

horobot_dormindo = r"""
        +---------------------------------+
        |  Desligando... Até a próxima    |
        |  sessão de estudos! zZzZ...     |
        +---------------------------------+
                 \
                  \
              .------.
         o -- |  _ _   | -- o
              '------'
             / [ OFF ] \
            /_________\
              | | | |
             '-----'
"""

horobot_nova_tarefa = r"""
        +---------------------------------+
        |  Tarefa Registrada!             |
        |  Mais um passo para o sucesso!  |
        +---------------------------------+
                 \
                  \
              .------.
         o -- |  ^_^  | -- o
              '------'
             / [ === ] \
            /_________\
              | | | |
             '-----'
"""