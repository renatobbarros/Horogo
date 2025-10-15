import json

cadeiras = "cadeiras.json"

with open(cadeiras, 'r', encoding='utf-8') as arq:
    cadeira_cadastrada = json.load('cadeiras.json')


print("HOROBOT: Aqui esta a situação de suas cadeiras.\n")
print('-----------------------------------------------')
print("Cadeira de {cadeira_cadastrada['nome']}")
print("Periodo: {cadeira_cadastrada['periodo']}")
print("Nos dias de {cadeira_cadastrada['dia']}, com o horario de {cadeira_cadastrada['horario']}")
print("Professor:{cadeira_cadastrada['professor']}")
print("Disciplina:{cadeira_cadastrada['disciplina']}")
print('------------------------------------------------')


