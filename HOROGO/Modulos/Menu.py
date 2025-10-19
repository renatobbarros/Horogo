import time
from HOROGO.Modulos.utilitarios import limpar_terminal, pagina_em_construcao
from HOROGO.Modulos import variaveis_globais

usuario = variaveis_globais.usuario

def boas_vindas_novo_usuario():
    limpar_terminal()
    print("HOROBOT: Seja bem-vindo(a) à agenda Horogo!")
    time.sleep(1)
    print("HOROBOT: Meu nome é Horobot e serei seu guia durante o seu tempo no HOROGO.")
    time.sleep(2)
    print("HOROBOT: Como você é novo por aqui, vou te explicar algumas coisas.")
    time.sleep(2)
    print("HOROBOT: A agenda Horogo é o melhor amigo do estudante durante seu tempo na universidade.")
    time.sleep(2)
    print("HOROBOT: Eu te acompanharei durante toda a sua jornada e te ajudarei a nunca perder um compromisso.")
    time.sleep(2)
    print("HOROBOT: Você iniciará no nível 1 e, conforme for usando o app, seu nível vai subindo.")
    time.sleep(2)
    print("HOROBOT: Agora, vamos para o seu menu principal!")
    time.sleep(3)
    
def menu_inicial():
    while True:
        limpar_terminal()
        
        print(f"Usuário: {usuario}\n", "--------------------------")
        print(f"Nível: ['Nivel'] | Universidade: ['Instituição']| Período: ['Periodo Atual']\n", "---------------------------------------------------")
        print('XP: [■■■■■■■■■■■■□□□□□□□□□]\n', "--------------------------------------------------------")
        print("Próximas Entregas:\n", "Pre-Release do Projeto: AGORA!!!!!!!!!!!!!!!!!!!!!!!!!!!! [O_o]\n", "--------------------------------------------------------")

        print("1. Notas", "      2. Cadeiras\n")
        print("3. Perfil", "      4. Mural\n")
        print("5. Calendário", "  6. Atualizar Conta\n")
        print("0. Sair do programa.")

        try:
            escolha_do_usuario = int(input("\nHOROBOT: O que você deseja fazer agora?\nUsuario: "))

            if escolha_do_usuario == 0:
                # A função de quit termina o codigo, fazendo que o programa feche.
                limpar_terminal()
                print("HOROBOT: Até a próxima!")
                time.sleep(2)
                limpar_terminal()
                quit()
                break
            elif 1 <= escolha_do_usuario <= 6:
                pagina_em_construcao()
                time.sleep(2)
            else:
                print("HOROBOT: Digite um valor válido (de 0 a 6).")
                time.sleep(2)
        
        except ValueError:
            print("HOROBOT: Ops! Parece que você não digitou um número. Tente novamente.")
            time.sleep(2)