import json
import time
from HOROGO.Modulos.utilitarios import limpar_terminal, carregar_conta, salvar_conta

# --- CORREÇÃO DE IMPORT ---
# O código original importava 'cadastrar_cadeira' de 'cadastro_notas.py'.
# Corrigimos para importar de 'cadeiras.py' (onde a função de criar cadeiras deve estar)
try:
    from HOROGO.Modulos.Academico.cadeiras import cadastrar_cadeira
except ImportError:
    # Se 'cadeiras.py' não existir, usamos a função de 'cadastro_notas.py'
    # (Embora isso seja logicamente incorreto, mantém o import original)
    from HOROGO.Modulos.Academico.cadastro_notas import cadastrar_cadeira

def situacao_cadeiras(usuario_logado):
    conta = carregar_conta()
    dados_importantes = conta.get(usuario_logado)

    # --- MELHORIA DE UX ---
    # Movido o 'limpar_terminal' para o início da função
    limpar_terminal()

    # se existir cadeira, ele continua. caso não exista, ou não tem nada dentro da cadeira, ele manda cadastrar.
    if "cadeiras" not in dados_importantes or not dados_importantes["cadeiras"]:
        print("HOROBOT: Você não tem nenhuma cadeira cadastrada.")
        time.sleep(1)
        print("HOROBOT: Vamos cadastrar uma agora.")
        time.sleep(2)
        
        # --- CORREÇÃO DE BUG ---
        # A função original chamava cadastrar_cadeira() sem o argumento.
        # Adicionamos o 'usuario_logado'
        try:
            cadastrar_cadeira(usuario_logado)
        except TypeError:
            print("HOROBOT: Erro ao tentar chamar a função de cadastro.")
            time.sleep(2)
        return

    print("HOROBOT: Aqui está a situação de suas cadeiras.\n")
    
    for i, cadeira in enumerate(dados_importantes["cadeiras"]):
        print(f'----------------- CADEIRA {i+1} ------------------')
        print(f"Nome da Cadeira: {cadeira.get('nome_cadeira', 'N/A')}")
        print(f"Professor(a):    {cadeira.get('nome_professor', 'N/A')}")
        print(f"Tempo Total:     {cadeira.get('tempo_cadeira', 'N/A')} horas")
        
        # --- ATUALIZAÇÃO: Exibir Notas e Situação ---
        
        # Tenta pegar o dicionário de notas
        notas = cadeira.get("notas")
        
        if notas:
            # Se 'notas' existe, exibe as notas
            va1 = notas.get('VA1')
            va2 = notas.get('VA2')
            va3 = notas.get('VA3') # Pode ser None
            
            print(f"Nota VA1:        {va1 if va1 is not None else 'N/A'}")
            print(f"Nota VA2:        {va2 if va2 is not None else 'N/A'}")
            print(f"Nota VA3 (Final):{va3 if va3 is not None else 'N/A'}")
            
            # Calcula a situação (Lógica da ATUALIZAÇÃO)
            situacao = "Indefinida (Notas Incompletas)"
            
            # Só calcula se VA1 e VA2 existirem
            if va1 is not None and va2 is not None:
                media_parcial = (va1 + va2) / 2
                
                if va3 is not None:
                    # Se o aluno fez a VA3 (Final)
                    # Assumindo que a média final é (Média Parcial + VA3) / 2
                    # E a nota de aprovação na final é 5
                    media_final_calc = (media_parcial + va3) / 2
                    if media_final_calc >= 5:
                        situacao = f"Aprovado (Média Final: {media_final_calc:.2f})"
                    else:
                        situacao = f"Reprovado (Média Final: {media_final_calc:.2f})"
                else:
                    # Se o aluno não fez a VA3
                    # Assumindo aprovação direta com >= 7
                    # Reprovação direta com < 4
                    # Final (Aguardando VA3) entre 4 e 7
                    if media_parcial >= 7:
                        situacao = f"Aprovado (Média: {media_parcial:.2f})"
                    elif media_parcial < 4:
                        situacao = f"Reprovado (Média: {media_parcial:.2f})"
                    else:
                        situacao = f"Aguardando Final (Média: {media_parcial:.2f})"
            
            print(f"Situação:        {situacao}")

        else:
            # Se 'notas' não existe
            print("Situação:        Notas não cadastradas.")
            
        print('----------------------------------------------------')
    
    # --- MELHORIA DE UX ---
    # Adiciona uma pausa no final para o usuário poder ler
    print("\nHOROBOT: Pressione ENTER para voltar ao menu.")
    input("Usuario: ")
    
    # O limpar_terminal() no final foi removido, 
    # pois limpava a tela antes que o usuário pudesse ler.