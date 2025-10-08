def cadastrar_cadeira(cadeira_cadastrada, nome, dia, horario, periodo, professor, disciplina):
    id_cadeira = 0

    if cadeira_cadastrada:

        id_cadeira = cadeira_cadastrada[+1]['id']

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
