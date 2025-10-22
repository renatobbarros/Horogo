import time
from HOROGO.Modulos.horobot import horobot_apresentacao
from HOROGO.Modulos.Autenticacao.login import sistema_login
from HOROGO.Modulos.Autenticacao.cadastro import sistema_cadastro 
from HOROGO.Modulos.utilitarios import limpar_terminal
from HOROGO.Modulos.Menu import menu_inicial

def main():
    """Função principal que organiza e controla todo programa. Se não funcionar, a gente chora."""
    limpar_terminal()
    print(horobot_apresentacao)
    time.sleep(1)
    print("HOROBOT: É um prazer te receber aqui!")
    time.sleep(1)
    print("HOROBOT: Serei seu amigo e guia durante sua jornada academica!")
    time.sleep(1)

    usuario_que_logou = None

    while True: 
        try:
            print("\nHOROBOT: Antes de mais nada, você já possui cadastro no HOROGO?")
            possuicadastro = int(input("1 - Sim \n2 - Não \nUSUARIO: "))
            limpar_terminal()
            if possuicadastro == 1:
                print("HOROBOT: Perfeito! me passe as seguintes informações para que eu te deixe onde parou da ultima vez")
                time.sleep(2)
                usuario_que_logou = sistema_login()
                break 
            elif possuicadastro == 2:
                usuario_que_logou = sistema_cadastro()
                break 
            else:
                print(f"O valor que você digitou: {possuicadastro}, não é uma opção válida. Por favor, digite 1 ou 2.")
                time.sleep(3)
        except ValueError:
            print("HOROBOT: Por favor, digite apenas números.")
            time.sleep(2)

    
    if usuario_que_logou:  
        menu_inicial(usuario_que_logou) 
    else:
        print("Até a proxima")

# O aplicativo so funciona se tiver essa condicional. O que acontece aqui e que ele procura pelo o arquivo main e chama a função de main (que ta ali encima) pra começar o programa.
if __name__ == "__main__":
    main()