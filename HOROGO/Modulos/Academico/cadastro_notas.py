import json
import time
from HOROGO.Modulos.utilitarios import limpar_terminal, carregar_conta, salvar_conta

def cadastrar_cadeira(usuario_logado):
    todas_as_contas = carregar_conta() 

    sair_loop = False
    while not sair_loop:
        limpar_terminal()
        print("HOROBOT: Agora, vamos preencher as notas de sua cadeira.")
        time.sleep(1)
        print("HOROBOT: Não se esqueça que so pode ser numeros!.\n")
        time.sleep(1)
        try:
            nota_1 = int(input("HOROBOT: Qual foi a nota da sua primeira VA?\n"))
            if nota_1 > 10:
                print('HOROBOT: Sua nota não pode ser acima de 10. Por favor, tente novamente.\n')
        except ValueError:
            print("HOROBOT: Sua nota deve ser um número. Tente novamente.")
        time.sleep(1)
        try:
            nota_2 = int(input("HOROBOT: Certo! Agora, qual foi a nota da sua segunda VA?\n"))
            if nota_2 > 10:
                print('HOROBOT: Sua nota não pode ser acima de 10. Por favor, tente novamente.\n')
        except ValueError:
            print("HOROBOT: Sua nota deve ser um número. Tente novamente.\n")

        time.sleep(1)

        print("HOROBOT: Você participou da 3º VA?")

        participei = input("Digite S se sim, e N se não participou.")

        if participei == "S":
            try:
                nota_3 = int(input("HOROBOT: No total, quantas horas tem essa cadeira?\nUsuario: "))
            except ValueError:
                print("HOROBOT: O tempo da cadeira deve ser um número. Tente novamente.")
                time.sleep(2)
            continue 
        
        print("\nHOROBOT: Nota validada com sucesso!")
        time.sleep(1)
        sair_loop = True


    novas_notas = {
        "VA1": nota_1,
        "VA2": nota_2,
        "VA3": nota_3
    }


    if "cadeiras" not in todas_as_contas[usuario_logado]:
        todas_as_contas[usuario_logado]["cadeiras"] = []

    todas_as_contas[usuario_logado]["cadeiras"].append(novas_notas)

    salvar_conta(todas_as_contas)
    
    print("HOROBOT: Cadeira adicionada ao seu perfil e salva com sucesso!")
    time.sleep(2)

