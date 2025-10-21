import json
import time
# Importando os mesmos utilitários de cadeiras.py
from HOROGO.Modulos.utilitarios import limpar_terminal, carregar_conta, salvar_conta

# O nome da função foi alterado para refletir o que ela faz
def cadastrar_notas(usuario_logado):
    todas_as_contas = carregar_conta() 

    # --- Lógica Chave ---
    # 1. Verificar se o usuário tem cadeiras cadastradas
    if "cadeiras" not in todas_as_contas[usuario_logado] or not todas_as_contas[usuario_logado]["cadeiras"]:
        limpar_terminal()
        print("HOROBOT: Você ainda não cadastrou nenhuma cadeira.")
        print("HOROBOT: Por favor, cadastre uma cadeira antes de adicionar notas.")
        time.sleep(3)
        return # Sai da função se não houver cadeiras

    # 2. Listar as cadeiras e pedir ao usuário para escolher uma
    lista_cadeiras = todas_as_contas[usuario_logado]["cadeiras"]
    cadeira_escolhida_ref = None # Esta será a referência para o dicionário da cadeira
    
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
                # 'break' não é necessário, 'cadeira_escolhida_ref' controla o loop
            else:
                print(f"HOROBOT: Número inválido. Digite um número entre 0 e {len(lista_cadeiras)}.")
                time.sleep(2)
        except ValueError:
            print("HOROBOT: Isso não é um número. Tente novamente.")
            time.sleep(2)

    # --- Lógica de `cadeiras.py`: Usar um loop 'while' para validação ---
    
    sair_loop = False
    nota_1 = None
    nota_2 = None
    nota_3 = None # 'None' será usado para indicar que o aluno não fez a VA3

    while not sair_loop:
        limpar_terminal()
        print(f"HOROBOT: Cadastrando notas para: {cadeira_escolhida_ref['nome_cadeira']}")
        print("HOROBOT: As notas devem ser números entre 0 e 10. Use '.' para decimais (ex: 8.5).\n")
        
        # --- Coletar NOTA 1 ---
        try:
            # Usar float para permitir notas decimais
            nota_1 = float(input("HOROBOT: Qual foi a nota da sua primeira VA?\nUsuario: "))
            if not (0 <= nota_1 <= 10):
                print('HOROBOT: Sua nota deve ser entre 0 e 10. Tente novamente.\n')
                time.sleep(2)
                continue # Reinicia o loop (pede VA1 de novo)
        except ValueError:
            print("HOROBOT: Sua nota deve ser um número. Tente novamente.")
            time.sleep(2)
            continue # Reinicia o loop

        # --- Coletar NOTA 2 ---
        try:
            nota_2 = float(input("HOROBOT: Certo! Agora, qual foi a nota da sua segunda VA?\nUsuario: "))
            if not (0 <= nota_2 <= 10):
                print('HOROBOT: Sua nota deve ser entre 0 e 10. Tente novamente.\n')
                time.sleep(2)
                continue # Reinicia o loop
        except ValueError:
            print("HOROBOT: Sua nota deve ser um número. Tente novamente.")
            time.sleep(2)
            continue # Reinicia o loop

        # --- Coletar NOTA 3 (Opcional) ---
        participei = input("HOROBOT: Você participou da 3º VA? (S/N)\nUsuario: ").strip().upper()

        if participei == "S":
            try:
                # Corrigido o prompt (não perguntava as horas)
                nota_3 = float(input("HOROBOT: Qual foi a nota da sua terceira VA?\nUsuario: "))
                if not (0 <= nota_3 <= 10):
                    print('HOROBOT: Sua nota deve ser entre 0 e 10. Tente novamente.\n')
                    time.sleep(2)
                    continue # Reinicia o loop
            except ValueError:
                print("HOROBOT: Sua nota deve ser um número. Tente novamente.")
                time.sleep(2)
                continue # Reinicia o loop
        
        elif participei == "N":
            nota_3 = None # Define como Nulo se não participou
        
        else:
            print("HOROBOT: Resposta inválida. Por favor, digite 'S' ou 'N'.")
            time.sleep(2)
            continue # Reinicia o loop

        # Se o código chegou até aqui, todas as entradas são válidas
        print("\nHOROBOT: Notas validadas com sucesso!")
        time.sleep(1)
        sair_loop = True # Termina o loop de validação


    # --- Lógica de `cadeiras.py` (adaptada): Criar o dicionário e salvar ---

    novas_notas = {
        "VA1": nota_1,
        "VA2": nota_2,
        "VA3": nota_3  # Salva o valor (float ou None)
    }

    # --- Correção Principal ---
    # Em vez de 'append', nós ATUALIZAMOS o dicionário da cadeira escolhida
    # Adicionando/atualizando a chave "notas" dentro dela
    cadeira_escolhida_ref["notas"] = novas_notas

    # Não precisamos mais do 'if "cadeiras" not in...' ou '.append'
    # pois estamos modificando um item existente

    salvar_conta(todas_as_contas)
    
    print("HOROBOT: Notas adicionadas ao seu perfil e salvas com sucesso!")
    time.sleep(2)