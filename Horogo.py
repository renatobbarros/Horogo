import os
import json

loop = 0

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
    # O input e comparado com os dados ja salvos, e caso esteja correto, o codigo autoriza a passar.
    print("HOROBOT: Perfeito! me passe as seguintes informações para que eu te deixe onde parou da ultima vez")
    usuario = "joaozinho gameplay"
    senha = "123"

    entrada_usuario = input(str("HOROBOT: Digite seu nome de usuario: "))
    entrada_senha = input(str("HOROBOT: Digite sua senha: "))

    if usuario == entrada_usuario and senha == entrada_senha: 
        loop = loop + 1
        print("HOROBOT: Você agora esta logado!")
    else:
        print("HOROBOT: Seu nome de usuario ou senha estão incorretos.")

def sistema_cadastro():
#    print("HOROBOT: Certo, vamos criar sua conta no HOROGO.")

#    criar_usuario = input(str("HOROBOT: Digite o nome de usuario que você deseja utilizar."))
#    criar_senha = input(str("HOROBOT: Muito bem, agora, crie a senha para sua conta."))

   



#Espaço para o login/cadastro de usuario
print("HOROBOT: Olá! é um prazer te receber aqui!")
print("HOROBOT: Meu nome é Horobot, serei seu amigo e guia durante sua jornada academica!")
print("HOROBOT: Antes de mais nada, você já possui cadastro no HOROGO?")

possuicadastro = int(input("1 - Sim \n2 - Não \nUSUARIO: "))

limparterminal()

while loop == 0:
    if possuicadastro == 1:
        sistema_login()
    elif possuicadastro == 2:
        sistema_cadastro()
    else: 
        print(f"O valor que você digitou: {possuicadastro}, não esta dentro das opçoes que te dei, por favor, digite apenas 1 ou 2 ")

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
        "id" : idnota,
        "avaliação" : tipodenota,
        "nota" : nota,
        "data" : datadanota,
        "cadeira" : lista_de_cadeiras,
    }
    notacadastrada.append(novanota)
    return notacadastrada