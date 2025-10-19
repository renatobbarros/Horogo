import time
from HOROGO.Modulos.horobot import horobot_apresentacao
from HOROGO.Modulos.Autenticacao.login import sistema_login
from HOROGO.Modulos.Autenticacao.cadastro import sistema_cadastro 
from HOROGO.Modulos.utilitarios import limpar_terminal
from HOROGO.Modulos.Menu import menu_inicial

def main():
    """Função principal que organiza e controla todo o fluxo do programa."""
    limpar_terminal()
    print(horobot_apresentacao)
    time.sleep(1)
    print("HOROBOT: É um prazer te receber aqui!")
    time.sleep(1)
    print("HOROBOT: Serei seu amigo e guia durante sua jornada academica!")
    time.sleep(1)

    # 1. CRIA UMA VARIÁVEL LOCAL PARA GUARDAR O RESULTADO DO LOGIN
    usuario_que_logou = None  # Começa como 'None' (vazio)

    while True: # Loop para garantir uma escolha válida
        try:
            print("\nHOROBOT: Antes de mais nada, você já possui cadastro no HOROGO?")
            possuicadastro = int(input("1 - Sim \n2 - Não \nUSUARIO: "))
            limpar_terminal()

            if possuicadastro == 1:
                print("HOROBOT: Perfeito! me passe as seguintes informações para que eu te deixe onde parou da ultima vez")
                time.sleep(2)
                
                # 2. A SUBSTITUIÇÃO ACONTECE AQUI!
                # A variável 'usuario_que_logou' recebe o que a função sistema_login() RETORNA.
                usuario_que_logou = sistema_login()
                
                break # Sai do loop da pergunta
            elif possuicadastro == 2:
                
                # E AQUI TAMBÉM, PARA O CADASTRO.
                usuario_que_logou = sistema_cadastro()

                break # Sai do loop da pergunta
            else:
                print(f"O valor que você digitou: {possuicadastro}, não é uma opção válida. Por favor, digite 1 ou 2.")
                time.sleep(3)
        except ValueError:
            print("HOROBOT: Por favor, digite apenas números.")
            time.sleep(2)

    # 3. AGORA, O FLUXO DEPENDE DA VARIÁVEL LOCAL, E NÃO DA GLOBAL
    if usuario_que_logou:  # Se a variável não for 'None', o login/cadastro deu certo
        menu_inicial(usuario_que_logou) # Passamos a variável para o menu
    else:
        print("Até a proxima")

# --- Ponto de Partida do Programa ---
# Esta linha garante que a função main() seja executada ao rodar o arquivo
if __name__ == "__main__":
    main()
