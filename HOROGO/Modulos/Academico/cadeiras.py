import time
from HOROGO.Modulos.utilitarios import limpar_terminal, carregar_conta, salvar_conta

def cadastrar_cadeira(usuario_logado):
    todas_as_contas = carregar_conta() 

    sair_loop = False
    while not sair_loop:
        limpar_terminal()
        print("HOROBOT: Vou te perguntar algumas coisas para adicionar essa disciplina.")
        time.sleep(1)
        print("HOROBOT: Nenhum nome deve ter mais de 50 caracteres.\n")
        time.sleep(1)
        nome_cadeira = input("HOROBOT: Qual é o nome da sua cadeira?\nUsuario: ")
        time.sleep(1)
        nome_professor = input("HOROBOT: Qual é o nome do professor(a) da cadeira?\nUsuario: ")
        time.sleep(1)
        
        try:
            tempo_cadeira = int(input("HOROBOT: No total, quantas horas tem essa cadeira?\nUsuario: "))
        except ValueError:
            print("HOROBOT: O tempo da cadeira deve ser um número. Tente novamente.")
            time.sleep(2)
            continue 

        if len(nome_cadeira) > 50 or len(nome_professor) > 50:
            limpar_terminal()
            print(f"HOROBOT: Nome da cadeira ({len(nome_cadeira)}) ou do professor ({len(nome_professor)}) é muito longo.")
            print("HOROBOT: Por favor, insira os dados novamente com menos de 50 caracteres.")
            time.sleep(4)
        else:
            print("\nHOROBOT: Cadeira validada com sucesso!")
            time.sleep(1)
            sair_loop = True


    nova_cadeira = {
        "nome_cadeira": nome_cadeira,
        "nome_professor": nome_professor,
        "tempo_cadeira": tempo_cadeira
    }


    if "cadeiras" not in todas_as_contas[usuario_logado]:
        todas_as_contas[usuario_logado]["cadeiras"] = []

    todas_as_contas[usuario_logado]["cadeiras"].append(nova_cadeira)

    salvar_conta(todas_as_contas)
    
    print("HOROBOT: Cadeira adicionada ao seu perfil e salva com sucesso!")
    time.sleep(2)

def cadastrar_notas(usuario_logado):
    todas_as_contas = carregar_conta() 

    if "cadeiras" not in todas_as_contas[usuario_logado]:
        limpar_terminal()
        print("HOROBOT: Você ainda não cadastrou nenhuma cadeira.")
        print("HOROBOT: Por favor, cadastre uma cadeira antes de adicionar notas.")
        time.sleep(3)
        return # Sai da função se não houver cadeiras

    
    lista_cadeiras = todas_as_contas[usuario_logado]["cadeiras"]
    cadeira_escolhida_ref = None #a referência para o dicionário da cadeira
    
    while cadeira_escolhida_ref is None:
        limpar_terminal()
        print("HOROBOT: Para qual cadeira você deseja cadastrar ou atualizar as notas?")
        
        # Enumera e exibe todas as cadeiras cadastradas
        for i, cadeira in enumerate(lista_cadeiras):
            print(f"  {i + 1}. {cadeira['nome_cadeira']}")
        print("\n  0. Voltar ao menu anterior")

        try:
            escolha_str = input("\nHOROBOT: Digite o número da cadeira: ")
            escolha_num = int(escolha_str)
            
            if escolha_num == 0:
                return # Volta ao menu
            
            # Verifica se a escolha está dentro do range da lista
            if 1 <= escolha_num <= len(lista_cadeiras):
                # Pega a referência direta ao dicionário da cadeira dentro da lista
                cadeira_escolhida_ref = lista_cadeiras[escolha_num - 1] 
            else:
                print(f"HOROBOT: Número inválido. Digite um número entre 0 e {len(lista_cadeiras)}.")
                time.sleep(2)
        except ValueError:
            print("HOROBOT: Isso não é um número. Tente novamente.")
            time.sleep(2)

    sair_loop = False
    nota_1 = None
    nota_2 = None
    nota_3 = None 

    while not sair_loop:
        limpar_terminal()
        print(f"HOROBOT: Cadastrando notas para: {cadeira_escolhida_ref['nome_cadeira']}")
        print("HOROBOT: As notas devem ser números entre 0 e 10. Use '.' para decimais (ex: 8.5).\n")
        
        
        try:
            nota_1 = float(input("HOROBOT: Qual foi a nota da sua primeira VA?\nUsuario: "))
            if not (0 <= nota_1 <= 10):
                print('HOROBOT: Sua nota deve ser entre 0 e 10. Tente novamente.\n')
                time.sleep(2)
                continue 
        except ValueError:
            print("HOROBOT: Sua nota deve ser um número. Tente novamente.")
            time.sleep(2)
            continue 

        try:
            nota_2 = float(input("HOROBOT: Certo! Agora, qual foi a nota da sua segunda VA?\nUsuario: "))
            if not (0 <= nota_2 <= 10):
                print('HOROBOT: Sua nota deve ser entre 0 e 10. Tente novamente.\n')
                time.sleep(2)
                continue 
        except ValueError:
            print("HOROBOT: Sua nota deve ser um número. Tente novamente.")
            time.sleep(2)
            continue 

        participei = input("HOROBOT: Você participou da 3º VA? (S/N)\nUsuario: ").strip().upper()

        if participei == "S":
            try:
                nota_3 = float(input("HOROBOT: Qual foi a nota da sua terceira VA?\nUsuario: "))
                if not (0 <= nota_3 <= 10):
                    print('HOROBOT: Sua nota deve ser entre 0 e 10. Tente novamente.\n')
                    time.sleep(2)
                    continue 
            except ValueError:
                print("HOROBOT: Sua nota deve ser um número. Tente novamente.")
                time.sleep(2)
                continue 
        
        elif participei == "N":
            nota_3 = None # Define como Nulo se não participou
        else:
            print("HOROBOT: Resposta inválida. Por favor, digite 'S' ou 'N'.")
            time.sleep(2)
            continue 

       
        print("\nHOROBOT: Notas validadas com sucesso!")
        time.sleep(1)
        sair_loop = True 

    novas_notas = {
        "VA1": nota_1,
        "VA2": nota_2,
        "VA3": nota_3  
    }

    cadeira_escolhida_ref["notas"] = novas_notas

    salvar_conta(todas_as_contas)
    
    print("HOROBOT: Notas adicionadas ao seu perfil e salvas com sucesso!")
    time.sleep(2)