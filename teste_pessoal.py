lista_de_cadeiras = []
lista_de_cadeiras = cadastrar_cadeira(
    cadeira_cadastrada = lista_de_cadeiras,
    nome="Cálculo 1",
    dia="Segunda",
    horario="08h - 10h",
    periodo="1º período",
    professor="Newton",
    disciplina="Matemática"
)
#Cadastro de notas
notas = []
def cadastronotas(usuario, notacadastrada, nota, lista_de_cadeiras ,datadanota, tipodenota):

    idnota = achar_id(notas)
#estou construindo no teste_pessoal
