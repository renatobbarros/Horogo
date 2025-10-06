import os
import json
#importei o time para colocar uma espera entre os prints para não cospir informações para os usuarios, evitando de assusta-los
import time
#importei o getpass para esconder as informações sensiveis, para usa-lo, basta substituir o input pelo getpass.getpass
import getpass
loop = 0

usuario = ""
senha = ""

logado = "NÃO"
#isaque, se sobrar tempo, vamos criar um desse pra cada fala importante do horobot!!!!!!!
# Beleza, nois faz tranquilo.
horobotola = """
          +-------------------------------------------------+
          |  Olá! Sou o Horobot, seu assistente de estudos. |
          +-------------------------------------------------+
                   \
                    \
              .------.
         o -- |  ^ ^ | -- o
              '------'
              /[ ** ]\   
             /________\
              | | | |
              '-----'
    """
def limparterminal():
    '''limpa o terminal de todo o texto que estiver dentro.'''
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
  
def achar_id(lista):
    '''encontra o ID dentro da lista de informações.'''
    if not lista:
        return 0 
    else:
        ultimo_item = lista[-1]
        ultimo_id = ultimo_item["id"]
        return ultimo_id + 1


def sistema_login():
    # O input e comparado com os dados ja salvos, e caso esteja correto, o codigo autoriza a passar(bolar o esquema de comparação).
    limparterminal()

    usuario
    senha 

    entrada_usuario = input(str("HOROBOT: Digite seu nome de usuario:\n"))
    time.sleep(1)

    entrada_senha = getpass.getpass(str("HOROBOT: Digite sua senha:\n"))
    time.sleep(1)
    limparterminal()
    #esse foi o unico jeito que lembrei para fazer voltar sem entrar em loop
    def validacaologin():
        if usuario == entrada_usuario and senha == entrada_senha: 
            print("HOROBOT: Você agora esta logado!")
            logado = "SIM"
        else:
            print("HOROBOT: Seu nome de usuario ou senha estão incorretos.")
            print("HOROBOT: Deseja fazer tentar novamente ou prefere criar uma conta? \n1 - tentar novamente\n2 - Criar conta\nUSUARIO: ")
            escolhanovamente = input(int())
        if escolhanovamente == 1:
            sistema_login()
        elif escolhanovamente == 2:
            sistema_cadastro()   
        else:
            print("HOROBOT: Por favor, digite apenas 1 ou 2")

    validacaologin()


def sistema_cadastro():
    '''O sistema cria as variaveis, e pede o input do usuario. Caso a senha seja maior que 12 caracteres, ele pede pra criar uma senha mais curta. Quando a conta e criada, as variaveis são jogadas na variavel de usuario e senha.'''
    print("HOROBOT: Certo, vamos criar sua conta no HOROGO.")

    time.sleep(2)

    criar_usuario = input(str("HOROBOT: Digite o nome de usuario que você deseja utilizar:\n"))

    loop_usuario = 0

    # Depois, vamo tentar fazer tudo em um loop so, se for possivel.
    while loop_usuario == 0:
        if len(criar_usuario) == 0 or len(criar_usuario) > 20:
            criar_usuario = input(str("HOROBOT: Seu nome de usuario contem mais do que 20 caracteres ou você colocou um nome vazio. Por favor, tente novamente.\n"))
        else: 
            criar_senha = getpass.getpass(str("HOROBOT: Muito bem, agora, crie a senha de ate 12 caracteres para sua conta:\n"))
            loop_usuario = 1
            time.sleep(1) 
    loop_senha = 0

    while loop_senha == 0:
        if len(criar_senha) > 12:
            criar_senha = getpass.getpass(str("HOROBOT: Sua senha contem muitos caracteres. Por favor, digite uma senha mais curta:\n"))
        elif len(criar_senha) == 0:
            criar_senha = getpass.getpass(str("HOROBOT: Você não preencheu sua senha, para sua segurança, digite uma senha:\n"))
        else:
            usuario = criar_usuario
            senha = criar_senha
            print("HOROBOT: Muito bem! Sua conta agora foi criada, vou te pedir pra colocar elas novamente só pra gente conferir se esta tudo ok.")
            time.sleep(1)
            loop_senha = 1
            sistema_login()


def boasvindasmenu():
    print("HOROBOT: Bem vindo ao menu do HOROGO!")
    print("HOROBOT: Aqui você podera escolher fazer o que quiser, a qualquer momento.")

limparterminal()
print(horobotola)
time.sleep(1)
print("HOROBOT: É um prazer te receber aqui!")
time.sleep(1)
print("HOROBOT: Serei seu amigo e guia durante sua jornada academica!")
time.sleep(1)
print("HOROBOT: Antes de mais nada, você já possui cadastro no HOROGO?")
time.sleep(1)
possuicadastro = int(input("1 - Sim \n2 - Não \nUSUARIO: "))

limparterminal()

while loop == 0:
    if possuicadastro == 1:
        print("HOROBOT: Perfeito! me passe as seguintes informações para que eu te deixe onde parou da ultima vez")
        time.sleep(2)
        limparterminal()
        sistema_login()
        loop = 1
    elif possuicadastro == 2:
        sistema_cadastro()
        loop = 1 
    else: 
        print(f"O valor que você digitou: {possuicadastro}, não esta dentro das opçoes que te dei, por favor, digite apenas 1 ou 2 ")

def main():
    if logado == "SIM":
        boasvindasmenu()
    else:
        print("Até a proxima")



#Desculpa, Isaque, me empolguei :(
# Relaxa, ta de boa. Empolgação e sucesso

def cadastrar_cadeira(cadeira_cadastrada, nome, dia, horario, periodo, professor, disciplina):
    id_cadeira = 0

    if cadeira_cadastrada:

        id_cadeira = cadeira_cadastrada[-1]['id']

    cadeira_nova = {
        'id': id_cadeira,
        'nome': nome,
        'dia': dia,
        'horario': horario,
        'periodo': periodo,
        'professor': professor,
        'disciplina': disciplina
    }
    cadeira_cadastrada.append(cadeira_nova)
    print(f"Sua cadeira com o ID {id_cadeira} foi criada com sucesso.")
    return cadeira_cadastrada

#minha parte verdadeira
#estou usando essa lista como base para a construção da minha parte
lista_de_cadeiras = []
lista_de_cadeiras = cadastrar_cadeira(
    cadeira_cadastrada=lista_de_cadeiras,
    nome="Cálculo 1",
    dia="Segunda",
    horario="08h - 10h",
    periodo="1º período",
    professor="Newton",
    disciplina="Matemática"
)
#Cadastro de notas
def cadastronotas(notacadastrada, nota, lista_de_cadeiras ,datadanota, tipodenota):

    idnota = achar_id(notacadastrada)

    novanota = {
        "usuario" : usuario,
        "id" : idnota,
        "avaliação" : tipodenota,
        "nota" : nota,
        "data" : datadanota,
        "cadeira" : lista_de_cadeiras,
    }
    notacadastrada.append(novanota)
    return notacadastrada