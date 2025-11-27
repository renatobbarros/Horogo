from ..repository.repositorio_usuario import repositorio_usuario

class servico_academico:
    def __init__(self, repositorio_usuario):
        self.repositorio = repositorio_usuario
    def criar_nova_cadeira(self, nome_cadeira, codigo_cadeira, periodo):
        '''Cria uma nova cadeira para o usuário'''
        # implementação fictícia apenas para ilustrar
        cadeira = {
            "nome": nome_cadeira,
            "codigo": codigo_cadeira,
            "periodo": periodo
        }
        return cadeira
    def adicionar_cadeira_ao_usuario(self, nome_usuario, cadeira):
        '''Adiciona uma cadeira ao usuário especificado'''
        usuario = self.repositorio.encontrar_usuario(nome_usuario)
        if usuario:
            if 'cadeiras' not in usuario.__dict__:
                usuario.cadeiras = []
            usuario.cadeiras.append(cadeira)
            self.repositorio.salvar_usuario(usuario)
            return True
        return False
    def atualizar_notas(self, nome_usuario, codigo_cadeira, notas):
        '''Atualiza as notas de uma cadeira específica para o usuário'''
        usuario = self.repositorio.encontrar_usuario(nome_usuario)
        if usuario and 'cadeiras' in usuario.__dict__:
            for cadeira in usuario.cadeiras:
                if cadeira['codigo'] == codigo_cadeira:
                    cadeira['notas'] = notas
                    self.repositorio.salvar_usuario(usuario)
                    return True
        return False