import time
from HOROGO.Modulos.utilitarios import Dados, Utilitarios
from HOROGO.Modulos.Academico.cadeiras import cadastrar_cadeira, cadastrar_notas
from HOROGO.Modulos.Academico.situacao_cadeiras import situacao_cadeiras

# ao definir o xp, certificar que essa parte esta funcionando
def boas_vindas_novo_usuario():
    Utilitarios.limpar_terminal()
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

def menu_notas(usuario_logado):

    todas_as_contas = Dados.carregar_conta()
    dados_usuario = todas_as_contas.get(usuario_logado, {})
    lista_de_cadeiras = dados_usuario.get("cadeiras", [])

    if not lista_de_cadeiras:
        Utilitarios.limpar_terminal()
        print("HOROBOT: Você não tem nenhuma cadeira cadastrada.")
        print("HOROBOT: É necessário cadastrar uma cadeira ANTES de gerenciar as notas.")
        print("\n1. Cadastrar cadeira agora")
        print("0. Voltar ao menu principal")
        try:
            escolha_sem_cadeira = int(input("\nUsuário: "))
            if escolha_sem_cadeira == 1:
                cadastrar_cadeira(usuario_logado)
            return 
        except ValueError:
            print("HOROBOT: Opção inválida.")
            time.sleep(2)
            return

    while True:
        Utilitarios.limpar_terminal()
        print("MENU DE NOTAS")
        print("=" * 25)
        print("1. Ver situação e médias")
        print("2. Adicionar ou atualizar notas")
        print("\n0. Voltar ao menu principal")

        try:
            escolha = int(input("\nHOROBOT: O que deseja fazer?\nUsuário: "))
            if escolha == 0:
                break 
            elif escolha == 1:
                situacao_cadeiras(usuario_logado) 
            elif escolha == 2:
                cadastrar_notas(usuario_logado)
            else:
                print("HOROBOT: Opção inválida. Tente novamente.")
                time.sleep(2)
        except ValueError:
            print("HOROBOT: Por favor, digite um número.")
            time.sleep(2)


def menu_cadeiras(usuario_logado):
    while True:
        Utilitarios.limpar_terminal()
        print("MENU DAS CADEIRAS")
        print("=" * 25)

        todas_as_contas = Dados.carregar_conta()
        dados_usuario = todas_as_contas.get(usuario_logado, {})
        lista_de_cadeiras = dados_usuario.get("cadeiras", [])

        if not lista_de_cadeiras:
            print("Você ainda não cadastrou nenhuma cadeira.\n")
            print("100. Cadastrar nova cadeira")
            print("0. Voltar ao menu principal")
            try:
                escolha = int(input("\nHOROBOT: O que deseja fazer?\nUsuário: "))
                if escolha == 100:
                    cadastrar_cadeira(usuario_logado)
                elif escolha == 0:
                    break
                else:
                    print("HOROBOT: Opção inválida. Tente novamente.")
                    time.sleep(2)
            except ValueError:
                print("HOROBOT: Por favor, digite um número.")
                time.sleep(2)
        else:
            print("Selecione uma cadeira para ver mais detalhes:\n")
            for i in range(0, len(lista_de_cadeiras), 2):
                cadeira1 = lista_de_cadeiras[i]
                texto1 = f"{i + 1}. {cadeira1['nome_cadeira']}"
                texto2 = ""
                if i + 1 < len(lista_de_cadeiras):
                    cadeira2 = lista_de_cadeiras[i + 1]
                    texto2 = f"{i + 2}. {cadeira2['nome_cadeira']}"
                print(f"{texto1:<35}{texto2}")
            print("\n" + "=" * 25)
            print("100. Cadastrar nova cadeira")
            print("0. Voltar ao menu principal")
            try:
                escolha = int(input("\nHOROBOT: O que deseja fazer?\nUsuário: "))
                if escolha == 0:
                    break
                elif escolha == 100:
                    cadastrar_cadeira(usuario_logado)
                elif 1 <= escolha <= len(lista_de_cadeiras):
                    cadeira_selecionada = lista_de_cadeiras[escolha - 1]
                    Utilitarios.limpar_terminal()
                    print(f"--- Detalhes de: {cadeira_selecionada['nome_cadeira']} ---")
                    print(f"Professor: {cadeira_selecionada['nome_professor']}")
                    print(f"Carga Horária: {cadeira_selecionada['tempo_cadeira']} horas")
                
                    if "notas" in cadeira_selecionada:
                        notas = cadeira_selecionada["notas"]
                        print("\n--- Notas ---")
                        print(f"  VA1: {notas.get('VA1', 'N/A')}")
                        print(f"  VA2: {notas.get('VA2', 'N/A')}")
                        print(f"  VA3: {notas.get('VA3', 'N/A')}")
                        input("\nPressione Enter para voltar...")
                else:
                    print("HOROBOT: Número de cadeira inválido.")
                    time.sleep(2)
            except ValueError:
                print("HOROBOT: Por favor, digite um número.")
                time.sleep(2)

def menu_inicial(usuario_logado):
    while True:
        todas_as_contas = Dados.carregar_conta()
        dados_usuario = todas_as_contas.get(usuario_logado, {})
        Utilitarios.limpar_terminal()
        
        print(f"Usuário: {dados_usuario.get('usuario', 'N/A')} \n--------------------------")

        print(f"Nível: {dados_usuario.get('nivel', 'N/A')} | Universidade: {dados_usuario.get('instituicao', 'N/A')} | Período: {dados_usuario.get('periodo_atual', 'N/A')}")
        print("---------------------------------------------------")
        print('XP: [■■■■■■■■■■■■■■■■■■■■■■■■□]')#implementar
        print("--------------------------------------------------------")
        print("Próximas Entregas:")
        print("Release do Projeto: AGORA!!!!!!!!!!!!!!!!!!!!!!!!!!!! [O_o]")
        print("--------------------------------------------------------\n")
        

        print("1. Notas", "       2. Cadeiras\n")
        print("3. Perfil", "      4. Mural\n")
        print("5. Calendário", "  6. Atualizar Conta\n")
        print("0. Sair do programa.")

        try:
            escolha_do_usuario = int(input("\nHOROBOT: O que você deseja fazer agora?\nUsuario: "))

            if escolha_do_usuario == 0:
                Utilitarios.limpar_terminal()
                print("HOROBOT: Até a próxima!")
                time.sleep(2)
                Utilitarios.limpar_terminal()
                quit()
                break 
            elif escolha_do_usuario == 1: 
                menu_notas(usuario_logado)
            elif escolha_do_usuario == 2:
                menu_cadeiras(usuario_logado)
            elif escolha_do_usuario in [3, 4, 5, 6]:
                Utilitarios.pagina_em_construcao()
            else:
                print("HOROBOT: Digite um valor válido (de 0 a 6).")
                time.sleep(2)
        except ValueError:
            print("HOROBOT: Ops! Parece que você não digitou um número. Tente novamente.")
            time.sleep(2)