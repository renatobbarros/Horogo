from HOROGO.Modulos.Autenticacao.login import nome_logado
import time
xp = 0
usuario = nome_logado 
def boas_vindas():
    print("HOROBOT: Seja bem-vindo(a) a agenda Horogo!")
    time.sleep(1)
    print("HOROBOT: Meu nome é horobot e serei seu guia durante o seu tempo no HOROGO")
    time.sleep(1)
    if xp == 0:
        print("HOROBOT: Como você é novo por aqui, vou te explicar algumas coisas")
        time.sleep(1)
        print("HOROBOT: A agenda Horogo é o melhor amigo do estudante durante seu tempo na universidade")
        time.sleep(1)
        print("HOROBOT: Eu te acompanharei durante toda a sua jornada e te ajudarei a nunca perder um compromisso, oportunidade ou avaliação")
        time.sleep(1)
        print("HOROBOT: Você iniciará no nivel 0 e com a classe de aprendiz de estudante, conforme você for adicionando notas, avaliações e compromissos, seu nivel e classe vão subindo")
        time.sleep(1)
        print("HOROBOT: Agora, preciso que você me informe quais cadeiras estaa cursando atualmente")
        time.sleep(1)
        cadastrar_cadeira()
    else:
        menu_inicial()


def menu_inicial():
    print(f"*-*" *25)
    print(f"Bem vindo {usuario}")
    print(nivel, universidade, periodo)
    print(xp)
    print ("proximas entregas")
    print(f"*-*" *25)

    
