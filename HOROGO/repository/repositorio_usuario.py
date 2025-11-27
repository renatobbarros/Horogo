class repositorio_usuario:
    def __init__(self, caminho_json):
        self.caminho_json = caminho_json
        self.usuarios = []
        self.carregar_usuarios()
    def carregar_usuarios(self):
        '''Carrega os usuários do arquivo JSON'''
        try:
            with open(self.caminho_json, 'r') as file:
                self.usuarios = json.load(file)
        except FileNotFoundError:
            self.usuarios = []
    def _salvar_json(self):
        '''Salva os usuários no arquivo JSON'''
        with open(self.caminho_json, 'w') as file:
            json.dump(self.usuarios, file, indent=4)
    def encontrar_usuario(self, username):
        '''Encontra um usuário pelo nome de usuário'''
        for usuario in self.usuarios:
            if usuario['username'] == username:
                return usuario
        return None
    def salvar_usuario(self, usuario):
        '''Salva um novo usuário ou atualiza um existente'''
        existente = self.encontrar_usuario(usuario['username'])
        if existente:
            self.usuarios.remove(existente)
        self.usuarios.append(usuario)
        self._salvar_json()