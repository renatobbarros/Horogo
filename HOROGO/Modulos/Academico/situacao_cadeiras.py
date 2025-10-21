import json
import time
from HOROGO.Modulos.utilitarios import limpar_terminal, carregar_conta, salvar_conta

try:
    from HOROGO.Modulos.Academico.cadeiras import cadastrar_cadeira
except ImportError:
    from HOROGO.Modulos.Academico.cadastro_notas import cadastrar_cadeira

def situacao_cadeiras(usuario_logado):
    conta = carregar_conta()
    dados_importantes = conta.get(usuario_logado)

    limpar_terminal()

    if "cadeiras" not in dados_importantes or not dados_importantes["cadeiras"]:
        print("HOROBOT: Você não tem nenhuma cadeira cadastrada.")
        time.sleep(1)
        print("HOROBOT: Vamos cadastrar uma agora.")
        time.sleep(2)
        
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
        
        notas = cadeira.get("notas")
        
        if notas:
            va1 = notas.get('VA1')
            va2 = notas.get('VA2')
            va3 = notas.get('VA3') # Pode ser None
            
            print(f"Nota VA1:        {va1 if va1 is not None else 'N/A'}")
            print(f"Nota VA2:        {va2 if va2 is not None else 'N/A'}")
            print(f"Nota VA3 (Final):{va3 if va3 is not None else 'N/A'}")
            
            situacao = "Indefinida (Notas Incompletas)"
            
            # Só calcula se VA1 e VA2 existirem
            if va1 is not None and va2 is not None:
                media_parcial = (va1 + va2) / 2
                if va3 is not None:
                    
                    media_final_calc = (media_parcial + va3) / 2
                    if media_final_calc >= 5:
                        situacao = f"Aprovado (Média Final: {media_final_calc:.2f})"
                    else:
                        situacao = f"Reprovado (Média Final: {media_final_calc:.2f})"
                else:
                    if media_parcial >= 7:
                        situacao = f"Aprovado (Média: {media_parcial:.2f})"
                    elif media_parcial < 4:
                        situacao = f"Reprovado (Média: {media_parcial:.2f})"
                    else:
                        situacao = f"Aguardando Final (Média: {media_parcial:.2f})"
            
            print(f"Situação:        {situacao}")

        else:
            print("Situação:        Notas não cadastradas.")
            
        print('----------------------------------------------------')
    
    print("\nHOROBOT: Pressione ENTER para voltar ao menu.")
    input("Usuario: ")