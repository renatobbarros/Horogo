class InterfaceHorobot:
    """Interface do Horobot com representações ASCII art."""

    @staticmethod
    def apresentar():
        print(horobot_apresentacao)

    @staticmethod
    def celebrar():
        print(horobot_celebracao)

    @staticmethod
    def confuso():
        print(horobot_confuso)

    @staticmethod
    def pensando():
        print(horobot_pensando)

    @staticmethod
    def dormindo():
        print(horobot_dormindo)

    @staticmethod
    def nova_tarefa():
        print(horobot_nova_tarefa)
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