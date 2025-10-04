#importações
import os
#Variaveis
sairloop = 0
# Funções primordiais
def limparterminal():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
  
def acharid(lista):
    if not lista:
        return 0 
    else:
        ultimoiten = lista[-1]
        ultimoid = ultimoiten["id"]
        return ultimoid + 1

#Espaço para o login/cadastro de usuario
print("\n\n\n\n\n\n\n\n\n\nHOROBOT: Olá! é um prazer te receber aqui!")
print("HOROBOT: Meu nome é Horobot, serei seu amigo e guia durante sua jornada academica!")
print("HOROBOT: Antes de mais nada, você já é possui cadastro no HOROGO?")

possuicadastro = int(input("1 - Sim \n2 - Não \nUSUARIO: "))

limparterminal()

while sairloop < 0:
    if possuicadastro == 1:
        print("HOROBOT: Perfeito! me passe as seguintes informações para que eu te deixe onde parou da ultima vez")
        emailusuario = input("HOROBOT: Digite seu Email: ")
        senhausuario = input("HOROBOT: Digite sua senha: ") #deixar a senha invisivel
        sairloop + 1 #bolar esquema pra sair do loop
        #bolar esquema para validar emaie e senha
    elif possuicadastro == 2:
        print("HOROBOT: Vou precisar pegar alguns dados seus para continuar")
        input("") #criar cadastro
        sairloop + 1
    else: 
        print(f"O valor que você digitou: {possuicadastro}, não esta dentro das opçoes que te dei, por favor, digite apenas 1 ou 2 ")

#Desculpa, Isaque, me empolguei :(

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

    idnota = acharid(notacadastrada)

    novanota = {
        "id" : idnota,
        "avaliação" : tipodenota,
        "nota" : nota,
        "data" : datadanota,
        "cadeira" : lista_de_cadeiras,
    }
    notacadastrada.append(novanota)
    return notacadastrada