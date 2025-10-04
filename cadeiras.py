def cadastrar_cadeira(cadeira_cadastrada, nome, dia, horario, periodo, professor, disciplina)
    id_cadeira = 1

    if cadeira_cadastrada:

        id_cadeira = cadeira_cadastrada[-1]["id"] + 1

        
    cadeira_nova = {
    "id": id_cadeira,
    "nome": "Como Aprender Python Na Hora Por Favor me Ajude Deus",
    "dia": "segunda",
    "horario": "De 8 as 12 da manha.",
    "periodo": "2 periodo",
    "professor": "Joao Python da Silva",
    "disciplina": "Aprendendo Python"
    }
    cadeira_cadastrada.append(cadeira_nova)
    print(f"Sua cadeira com o ID {id_cadeira} foi criada com sucesso.")
    