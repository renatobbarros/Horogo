#### (devido a alta demanda de trabalhos e o curto espaço de tempo para a realização de todos, utilizamos o gemini *SOMENTE* para saber quais classes devemos criar, a criação de todo o progrma em geral e principalmente das classes será de autoria propria, sem ajuda de I.A)

Plano de Refatoração POO - Projeto Horogo

1. Objetivo Principal

O objetivo desta refatoração é migrar o projeto Horogo de um paradigma estruturado (múltiplas funções soltas) para uma arquitetura Orientada a Objetos (POO) limpa e robusta.

Por que fazer isso?

Separação de Responsabilidades (SRP): Cada classe terá uma única responsabilidade. Isso torna o código drasticamente mais fácil de entender e depurar.

Manutenibilidade: Mudar uma regra de negócio (ex: cálculo de média) não exigirá mais mexer em arquivos de interface (print/input).

Extensibilidade: Adicionar novas funcionalidades (como uma interface gráfica - GUI) será infinitamente mais fácil, pois a lógica do "motor" do programa estará completamente separada da "aparência".

Testabilidade: Classes pequenas e focadas são fáceis de testar de forma isolada.

2. A Nova Arquitetura (O Design-Alvo)

Vamos organizar o projeto em 5 camadas lógicas. Cada camada só pode "conversar" com a camada adjacente, nunca pulando etapas (ex: a Interface nunca falará com o Repositório).

Camada de Modelos (Models):

Classes: Usuario, Cadeira, Nota.

Função: Apenas guardar dados. São os "moldes" do nosso sistema.

Camada de Repositório (Repository):

Classe: RepositorioUsuario.

Função: É a única classe que sabe ler e escrever no conta.json. Se um dia mudarmos para um banco SQL, esta é a única classe que precisará ser alterada.

Camada de Serviço (Services):

Classes: ServicoAutenticacao, ServicoAcademico.

Função: Contém a lógica de negócio ("cérebro"). Validações, cálculos, regras. Não contém NENHUM print ou input.

Camada de Interface (Views):

Classes: InterfaceConsole, InterfaceHorobot, InterfaceAutenticacao, InterfaceAcademica, InterfaceMenuPrincipal.

Função: É a única camada que usa print, input, getpass, os.system. Ela é "burra": apenas exibe dados e captura a entrada do usuário, passando o trabalho sujo para os Serviços.

Camada de Aplicação (App):

Classe: AplicacaoHorogo (dentro do app.py).

Função: O "maestro". Inicia o programa e coordena o fluxo de alto nível (ex: mostra apresentação, chama autenticação, inicia o menu principal).

3. Plano de Ação (Tarefas do "Trello")

Abaixo está o checklist detalhado para criar cada classe da nova arquitetura.

Camada 1: Modelos (Os Dados)

O primeiro passo é definir as estruturas de dados.

[ ] Criar nota.py

[ ] Classe Nota:

Atributos: va1: float, va2: float, va3: float | None

Métodos:

__init__(self, va1, va2, va3): Construtor.

to_dict(self) -> dict: Converte o objeto para um dicionário para salvar no JSON.

calcular_media_parcial(self) -> float | None: (Lógica de (va1+va2)/2).

calcular_media_final(self) -> float | None: (Lógica de (media_parcial+va3)/2).

get_situacao(self) -> str: (Toda a lógica if/elif/else de Aprovado/Reprovado que estava em situacao_cadeira.py).

@classmethod from_dict(cls, data: dict): Cria um objeto Nota a partir de um dicionário (lido do JSON).

[ ] Criar cadeira.py

[ ] Classe Cadeira:

Atributos: nome_cadeira: str, nome_professor: str, tempo_cadeira: int, notas: Nota | None (guarda um objeto Nota).

Métodos:

__init__(self, nome_cadeira, nome_professor, tempo_cadeira, notas=None): Construtor.

adicionar_notas(self, va1, va2, va3): Cria um objeto Nota e o armazena em self.notas.

to_dict(self) -> dict: Converte para dicionário JSON (chama self.notas.to_dict()).

get_notas_formatadas(self) -> str: (Lógica de exibição de notas de situacao_cadeira.py).

get_situacao_formatada(self) -> str: (Chama self.notas.get_situacao() se self.notas existir).

@classmethod from_dict(cls, data: dict): Cria um objeto Cadeira a partir de um dicionário (e chama Nota.from_dict para as notas).

[ ] Criar usuario.py

[ ] Classe Usuario:

Atributos: usuario: str, senha: str, instituicao: str, periodo: int, xp: int, nivel: int, cadeiras: list (lista de objetos Cadeira).

Métodos:

__init__(...): Construtor que recebe todos os atributos (com valores padrão para xp, nivel e cadeiras).

verificar_senha(self, senha_digitada: str) -> bool: (Lógica de self.senha == senha_digitada.strip()).

adicionar_cadeira(self, cadeira_obj: Cadeira): (Lógica: self.cadeiras.append(cadeira_obj)).

get_cadeiras(self) -> list[Cadeira]: (Lógica: return self.cadeiras).

to_dict(self) -> dict: Converte para JSON (e chama c.to_dict() para cada cadeira na lista).

@classmethod from_dict(cls, data: dict): Cria um Usuario a partir de um dicionário (e chama Cadeira.from_dict para cada cadeira na lista).

Camada 2: Repositório (Acesso ao JSON)

Onde a classe Dados do utilitario.py será absorvida.

[ ] Criar repositorio.py

[ ] Classe RepositorioUsuario:

Atributos: caminho_arquivo: str

Métodos:

__init__(self, caminho_arquivo="conta.json").

_carregar_json_bruto(self) -> dict: (Lógica de Dados.carregar_conta, mas deve raise Exception em vez de print em caso de erro).

_salvar_json_bruto(self, dados_dict: dict): (Lógica de Dados.salvar_conta, mas deve raise Exception em vez de print).

_carregar_objetos_usuario(self) -> dict[str, Usuario]: (Chama _carregar_json_bruto e usa Usuario.from_dict para converter tudo em objetos Usuario).

_salvar_objetos_usuario(self, todos_usuarios: dict[str, Usuario]): (Recebe objetos Usuario, usa usuario.to_dict e chama _salvar_json_bruto).

encontrar_usuario(self, nome_usuario: str) -> Usuario | None: (Método público que carrega e retorna um único objeto Usuario ou None).

salvar_usuario(self, usuario: Usuario): (Método público que carrega tudo, atualiza o usuário, e salva tudo).

Camada 3: Serviços (A Lógica de Negócio)

Onde a "inteligência" do cadastro.py e academico.py irá morar. Sem print/input aqui.

[ ] Criar servico_auth.py

[ ] Classe ServicoAutenticacao:

__init__(self, repositorio: RepositorioUsuario).

login(self, nome_usuario, senha) -> Usuario | None: (Chama repo.encontrar_usuario e usuario.verificar_senha).

cadastrar_usuario(self, nome, senha, instituicao, periodo) -> Usuario | str: (Contém toda a lógica de validação de cadastro.py: tamanho do nome, tamanho da senha, período é dígito, usuário já existe, etc. Retorna o objeto Usuario em sucesso ou uma str de erro em falha).

[ ] Criar servico_academico.py

[ ] Classe ServicoAcademico:

__init__(self, repositorio: RepositorioUsuario).

criar_nova_cadeira(self, nome_cadeira, nome_prof, tempo) -> Cadeira | str: (Valida os dados da cadeira. Retorna o objeto Cadeira em sucesso ou str de erro).

adicionar_cadeira_ao_usuario(self, usuario: Usuario, cadeira: Cadeira): (Chama usuario.adicionar_cadeira(cadeira) e self.repositorio.salvar_usuario(usuario)).

atualizar_notas(self, usuario: Usuario, cadeira: Cadeira, va1, va2, va3): (Chama cadeira.adicionar_notas(...) e self.repositorio.salvar_usuario(usuario)).

Camada 4: Views (A Interface do Console)

Onde Menu.py, horobot.py e o resto do utilitario.py serão absorvidos.

[ ] Criar interface_console.py

[ ] Classe InterfaceConsole: (A única classe que usa os, time, input, print, getpass).

Métodos: limpar_tela(), exibir_mensagem(msg, autor, delay), obter_input(prompt), obter_senha(prompt), pausar_tela().

[ ] Criar interface_horobot.py

[ ] Classe InterfaceHorobot:

__init__(self, console: InterfaceConsole).

Mover todas as artes ASCII (ex: _APRESENTACAO) para atributos privados.

Criar métodos públicos (ex: exibir_apresentacao()) que chamam self.console.exibir_arte().

Absorver pagina_em_construcao de utilitario.py (renomear para exibir_em_construcao()).

[ ] Criar interface_auth.py

[ ] Classe InterfaceAutenticacao:

__init__(self, servico_auth: ServicoAutenticacao, console: InterfaceConsole, horobot: InterfaceHorobot).

executar_login(self) -> Usuario | None: (Substitui sistema_login. Contém o while True de print/input. Chama servico.login para a lógica. Chama _exibir_menu_login_falho em caso de erro).

executar_cadastro(self) -> Usuario | None: (Substitui sistema_cadastro. Contém todos os while True de print/input. Chama servico.cadastrar_usuario e trata o retorno, que pode ser Usuario ou str de erro).

_exibir_menu_login_falho(self) -> str: (Substitui tratar_login_falho. Retorna uma "ação" como string, ex: "TENTAR_NOVAMENTE" ou "CADASTRO").

[ ] Criar interface_academica.py

[ ] Classe InterfaceAcademica:

__init__(self, servico_academico: ServicoAcademico, console: InterfaceConsole, horobot: InterfaceHorobot).

executar_menu_notas(self, usuario: Usuario): (Substitui menu_notas de Menu.py).

executar_menu_cadeiras(self, usuario: Usuario): (Substitui menu_cadeiras de Menu.py. Inclui a lógica de 2 colunas).

executar_menu_cadastrar_cadeira(self, usuario: Usuario): (Substitui cadastrar_cadeira de academico.py. Contém os print/input. Chama servico.criar_nova_cadeira e servico.adicionar_cadeira_ao_usuario).

executar_menu_cadastrar_notas(self, usuario: Usuario): (Substitui cadastrar_notas de academico.py. Chama servico.atualizar_notas).

executar_situacao_cadeiras(self, usuario: Usuario): (Substitui situacao_cadeiras. Apenas faz o loop nas usuario.get_cadeiras() e chama os métodos de formatação cadeira.get_notas_formatadas() e cadeira.get_situacao_formatada()).

[ ] Criar interface_menu.py

[ ] Classe InterfaceMenuPrincipal:

__init__(...): Recebe console, horobot, repo_usuario, interface_academica.

executar(self, usuario: Usuario): (O while True principal do programa. Substitui menu_inicial de Menu.py).

_exibir_dashboard(self, usuario: Usuario): (O print do menu principal com os dados do usuário).

Camada 5: A Aplicação (O Ponto de Partida)

[ ] Refatorar app.py

[ ] Criar a classe AplicacaoHorogo.

[ ] __init__(...): Recebe as interfaces principais (console, horobot, interface_auth, menu_principal).

run(self): (Contém a lógica de apresentação e o while True que chama _iniciar_autenticacao e depois menu_principal.executar).

_iniciar_autenticacao(self) -> Usuario | None: (Contém o while True que pergunta "Já possui cadastro?").

[ ] Reescrever a função main() para ser a Fábrica:

É aqui que todos os objetos serão criados e "injetados" uns nos outros.

Exemplo:

def main():
    # 1. Criar I/O
    console = InterfaceConsole()
    horobot = InterfaceHorobot(console)

    # 2. Criar Dados
    repo = RepositorioUsuario("conta.json")

    # 3. Criar Lógica
    serv_auth = ServicoAutenticacao(repo)
    serv_acad = ServicoAcademico(repo)

    # 4. Criar Interfaces
    if_auth = InterfaceAutenticacao(serv_auth, console, horobot)
    if_acad = InterfaceAcademica(serv_acad, console, horobot)
    if_menu = InterfaceMenuPrincipal(console, horobot, repo, if_acad)

    # 5. Criar e Rodar a Aplicação
    app = AplicacaoHorogo(console, horobot, if_auth, if_menu)
    app.run()





## Arquivo: academicos.py (Sugestão de novo nome)
Tarefa 1: Criar a Classe Nota (Model)
Vamos começar criando um modelo para as notas. Em vez de um dicionário {"VA1": 8.5}, vamos criar uma classe que pode ter lógicas futuras, como cálculo de média.

Classe: Nota

Responsabilidade: Guardar e gerenciar as notas de UMA cadeira.

Atributos (Dados):

va1: float

va2: float

va3: float | None (usamos None se o aluno não fez)

Métodos (Funções):

__init__(self, va1=0.0, va2=0.0, va3=None): O construtor, para criar o objeto.

calcular_media(self) -> float: (Método futuro) Uma função que calcula a média das notas. Por enquanto, pode só pass.

to_dict(self) -> dict: Um método que converte a classe em um dicionário simples (ex: {"VA1": 8.5, ...}). Isso é crucial para salvar em JSON.

Tarefa 2: Criar a Classe Cadeira (Model)
Esta é a classe principal. Ela vai representar UMA disciplina/cadeira.

Classe: Cadeira

Responsabilidade: Guardar todas as informações de UMA cadeira.

Atributos (Dados):

nome_cadeira: str

nome_professor: str

tempo_cadeira: int

notas: Nota (Ela não terá um dicionário de notas, ela terá um objeto Nota)

Métodos (Funções):

__init__(self, nome_cadeira, nome_professor, tempo_cadeira): O construtor. Note que ele não recebe as notas no início.

adicionar_notas(self, va1, va2, va3): Recebe as notas, cria um objeto Nota e o armazena no atributo self.notas.

get_media(self) -> float: (Método futuro) Chama self.notas.calcular_media() para obter a média.

to_dict(self) -> dict: Converte a Cadeira em um dicionário para salvar no JSON. (Ex: {"nome_cadeira": "Cálculo", ..., "notas": self.notas.to_dict()}).

Tarefa 3: Criar a Classe ServicoAcademico (Service)
Esta classe terá a lógica de negócio. Ela não vai usar print ou input. Ela apenas executa tarefas e retorna resultados.

Classe: ServicoAcademico

Responsabilidade: Orquestrar as ações académicas (criar e atualizar cadeiras).

Métodos (Funções):

criar_nova_cadeira(self, nome_cadeira, nome_professor, tempo_cadeira) -> Cadeira:

Recebe os dados (que vieram da interface do usuário).

Valida os dados (ex: len(nome_cadeira) > 50). Se for inválido, pode retornar None ou levantar uma exceção (vamos retornar None por enquanto).

Cria um novo objeto Cadeira com os dados validados.

Retorna o objeto Cadeira recém-criado.

adicionar_cadeira_ao_usuario(self, usuario, cadeira):

Recebe um objeto Usuario (que definiremos depois) e um objeto Cadeira.

Adiciona a cadeira à lista de cadeiras do usuario. (Ex: usuario.cadeiras.append(cadeira)).

atualizar_notas(self, cadeira, va1, va2, va3):

Recebe o objeto Cadeira que o usuário escolheu e as novas notas.

Chama o método cadeira.adicionar_notas(va1, va2, va3) para atualizar o objeto.

Tarefa 4: Criar a Classe InterfaceCadeira (View / UI)
Esta classe terá toda a lógica de console (print, input, time.sleep). Ela é o "rosto" do seu código.

Classe: InterfaceCadeira

Responsabilidade: Exibir menus, pedir dados ao usuário e chamar o ServicoAcademico para fazer o trabalho.

Atributos (Dados):

servico_academico: ServicoAcademico (Ela precisa de uma "cópia" do serviço para poder usá-lo).

Métodos (Funções):

__init__(self, servico): Construtor que recebe o ServicoAcademico e o armazena em self.servico_academico.

exibir_menu_cadastrar_cadeira(self, usuario_logado):

Esta função conterá todo o loop while da sua cadastrar_cadeira original, com os print e input.

Quando os dados (nome, professor, tempo) forem validados, ela chamará o serviço: nova_cadeira = self.servico_academico.criar_nova_cadeira(...)

Se nova_cadeira for criada com sucesso, ela chama o outro serviço: self.servico_academico.adicionar_cadeira_ao_usuario(usuario_logado, nova_cadeira)

Por fim, ela imprimirá a mensagem de sucesso.

exibir_menu_cadastrar_notas(self, usuario_logado):

Esta função conterá todo o loop while da sua cadastrar_notas original.

Ela exibirá a lista de cadeiras (ex: usuario_logado.get_cadeiras()).

Após o usuário escolher a cadeira e digitar as notas, ela chamará o serviço: cadeira_obj_escolhido = usuario_logado.cadeiras[escolha - 1] self.servico_academico.atualizar_notas(cadeira_obj_escolhido, n1, n2, n3)

Imprimirá a mensagem de sucesso.


## Arquivo: academicos.py (Onde as classes Nota e Cadeira vivem)
Este arquivo será atualizado com a nova lógica de negócio que estava "escondida" no seu situacao_cadeira.py.

Tarefa 1: Adicionar "Inteligência" à Classe Nota
Vamos mover toda a lógica de cálculo de média e situação para dentro da classe Nota, pois é ela quem "sabe" como deve ser calculada.

Classe: Nota (Modificação)

Novos Métodos a Adicionar:

calcular_media_parcial(self) -> float | None

Responsabilidade: Calcular a média entre VA1 e VA2.

Lógica:

if self.va1 is not None and self.va2 is not None:

return (self.va1 + self.va2) / 2

else:

return None

calcular_media_final(self) -> float | None

Responsabilidade: Calcular a média final (se a VA3 existir).

Lógica:

media_parcial = self.calcular_media_parcial()

if media_parcial is not None and self.va3 is not None:

return (media_parcial + self.va3) / 2

else:

return None

get_situacao(self) -> str

Responsabilidade: Conter toda a lógica de if/elif/else para determinar a situação do aluno.

Lógica:

media_final = self.calcular_media_final()

if media_final is not None:

if media_final >= 5: return f"Aprovado (Média Final: {media_final:.2f})"

else: return f"Reprovado (Média Final: {media_final:.2f})"

media_parcial = self.calcular_media_parcial()

if media_parcial is not None:

if media_parcial >= 7: return f"Aprovado (Média: {media_parcial:.2f})"

elif media_parcial < 4: return f"Reprovado (Média: {media_parcial:.2f})"

else: return f"Aguardando Final (Média: {media_parcial:.2f})"

return "Indefinida (Notas Incompletas)"

Tarefa 2: Adicionar "Inteligência" à Classe Cadeira
A classe Cadeira deve ser capaz de formatar sua própria exibição de status, delegando o cálculo para a classe Nota.

Classe: Cadeira (Modificação)

Novos Métodos a Adicionar:

get_notas_formatadas(self) -> str

Responsabilidade: Retornar uma string com as notas formatadas.

Lógica:

if not self.notas: return "Notas não cadastradas."

va1 = self.notas.va1 if self.notas.va1 is not None else 'N/A'

va2 = self.notas.va2 if self.notas.va2 is not None else 'N/A'

va3 = self.notas.va3 if self.notas.va3 is not None else 'N/A'

return f"Nota VA1: {va1}\nNota VA2: {va2}\nNota VA3 (Final): {va3}"

get_situacao_formatada(self) -> str

Responsabilidade: Retornar a string final da situação da cadeira.

Lógica:

if not self.notas: return "Notas não cadastradas."

return self.notas.get_situacao()

Arquivo: interfaces.py (ou InterfaceCadeira no seu academicos.py)
Esta classe será a nova "casa" da sua função situacao_cadeiras, mas agora ela será uma função "burra", que só sabe como printar. Toda a lógica complexa foi movida para os modelos.

Tarefa 3: Criar o Método exibir_situacao_cadeiras
Classe: InterfaceCadeira (a mesma que definimos antes)

Novo Método: exibir_situacao_cadeiras(self, usuario_logado)

Responsabilidade: Apenas exibir os dados. Não faz cálculos.

Lógica:

Recebe o objeto usuario_logado (da classe Usuario, que definiremos depois).

Pega a lista de cadeiras: lista_cadeiras = usuario_logado.get_cadeiras() (Este será um método da classe Usuario).

Utilitarios.limpar_terminal()

Verifica se a lista está vazia: if not lista_cadeiras:

print("HOROBOT: Você não tem nenhuma cadeira cadastrada.")

print("HOROBOT: Você será redirecionado para cadastrar uma...")

time.sleep(3)

Importante: A interface chama outra função da própria interface: self.exibir_menu_cadastrar_cadeira(usuario_logado)

return

Se a lista não estiver vazia, ela faz o loop: for i, cadeira in enumerate(lista_cadeiras):

Dentro do loop, ela apenas imprime chamando os atributos e métodos dos objetos:

print(f'----------------- CADEIRA {i+1} ------------------')

print(f"Nome da Cadeira: {cadeira.nome_cadeira}")

print(f"Professor(a): {cadeira.nome_professor}")

print(f"Tempo Total: {cadeira.tempo_cadeira} horas")

print(cadeira.get_notas_formatadas())

print(f"Situação: {cadeira.get_situacao_formatada()}")

print('----------------------------------------------------')

No final:

print("\nHOROBOT: Pressione ENTER para voltar ao menu.")

input("Usuario: ")

## usuario.py (Novo Arquivo - O "Modelo" de Dados)
Primeiro, vamos definir o que é um "Usuário". Esta classe não faz nada, ela apenas é (guarda dados).

Tarefa 1: Criar a Classe Usuario
Classe: Usuario

Responsabilidade: Representar os dados de um único usuário.

Atributos (Dados):

usuario: str

senha: str (No futuro, você aprenderá a "hashear" isso)

instituicao: str

periodo_atual: int

cadeiras: list (Esta será uma lista de objetos Cadeira)

xp: int

nivel: int

Métodos (Funções):

__init__(self, usuario, senha, instituicao, periodo, xp=0, nivel=1, cadeiras=None): O construtor para criar um novo objeto Usuario. Se cadeiras for None, ele deve inicializá-lo como [].

verificar_senha(self, senha_digitada: str) -> bool:

Lógica: return self.senha == senha_digitada.strip()

adicionar_cadeira(self, cadeira_obj):

Lógica: self.cadeiras.append(cadeira_obj)

get_cadeiras(self) -> list:

Lógica: return self.cadeiras

to_dict(self) -> dict:

Responsabilidade: Converter o objeto Usuario de volta para um dicionário que pode ser salvo em JSON.

Lógica: return {"usuario": self.usuario, "senha": self.senha, ...} (Cuidado: se self.cadeiras for uma lista de objetos Cadeira, você precisará chamar cadeira.to_dict() para cada um deles).

@classmethod from_dict(cls, data: dict):

Responsabilidade: Um método de "fábrica" que cria um objeto Usuario a partir de um dicionário lido do JSON.

Arquivo: repositorio.py (Novo ou Atualizado - O "Acesso aos Dados")
Esta classe é a única que sabe que seus dados estão em um arquivo JSON. Se amanhã você mudar para um banco de dados SQL, esta é a única classe que você precisará alterar.

Tarefa 2: Criar a Classe RepositorioUsuario
Classe: RepositorioUsuario

Responsabilidade: Ler e salvar dados de usuários no conta.json. Ela não sabe por quê, ela apenas faz.

Atributos:

caminho_arquivo: str

Métodos:

__init__(self, caminho_arquivo="conta.json"): Construtor.

carregar_contas(self) -> dict[str, Usuario]:

Lógica: Chama Dados.carregar_conta(). Em vez de retornar o dicionário cru, ele itera por esse dicionário e usa Usuario.from_dict() para criar um novo dicionário de objetos Usuario (ex: {"renato": <Objeto Usuario renato>}).

salvar_contas(self, todos_os_usuarios: dict[str, Usuario]):

Lógica: Recebe um dicionário de objetos Usuario. Converte cada objeto de volta para um dicionário usando usuario.to_dict(). Salva esse novo dicionário de dicionários no JSON usando Dados.salvar_conta().

encontrar_usuario(self, nome_usuario: str) -> Usuario | None:

Lógica: contas = self.carregar_contas(). Retorna contas.get(nome_usuario).

salvar_usuario(self, usuario: Usuario):

Lógica: contas = self.carregar_contas(). contas[usuario.usuario] = usuario. self.salvar_contas(contas).

Arquivo: servico_auth.py (Novo Arquivo - A "Lógica de Negócio")
Esta classe toma as decisões. Ela é o "cérebro". Ela não usa print ou input. Ela apenas recebe dados, aplica regras e retorna um resultado.

Tarefa 3: Criar a Classe ServicoAutenticacao
Classe: ServicoAutenticacao

Responsabilidade: Validar login e regras de cadastro.

Atributos:

repositorio: RepositorioUsuario

Métodos:

__init__(self, repositorio: RepositorioUsuario): Construtor.

login(self, nome_usuario: str, senha_digitada: str) -> Usuario | None:

Lógica: Pega o usuário com self.repositorio.encontrar_usuario(nome_usuario). Se o usuário existir E usuario.verificar_senha(senha_digitada) for True, retorna o usuario. Senão, retorna None.

cadastrar_usuario(self, nome, senha, instituicao, periodo) -> (Usuario | str):

Lógica:

Valida os dados: if not (0 < len(nome) <= 20): return "Erro: Usuário inválido"

Valida a senha: if not (0 < len(senha) <= 12): return "Erro: Senha inválida"

Verifica se existe: if self.repositorio.encontrar_usuario(nome): return "Erro: Usuário já existe"

Se tudo estiver OK:

Cria o objeto: novo_usuario = Usuario(nome, senha, instituicao, periodo)

Salva no repositório: self.repositorio.salvar_usuario(novo_usuario)

Retorna o objeto: return novo_usuario

Arquivo: interface_auth.py (Novo Arquivo - A "Interface de Console")
Esta classe é a nova "casa" de todo o seu código original. Sua única responsabilidade é exibir prints e capturar inputs. Ela não toma decisões, apenas chama o "Serviço" para fazer isso.

Tarefa 4: Criar a Classe InterfaceAutenticacao
Classe: InterfaceAutenticacao

Responsabilidade: Lidar com toda a interação de console para login e cadastro.

Atributos:

servico_auth: ServicoAutenticacao

Métodos:

__init__(self, servico: ServicoAutenticacao): Construtor.

executar_login(self) -> Usuario | None:

Lógica: Contém o while True de sistema_login(). Pede usuário e senha.

Chama usuario_obj = self.servico_auth.login(usuario_digitado, senha_digitada).

Se usuario_obj for um Usuario, imprime "Logado com sucesso!" e return usuario_obj.

Se for None, imprime "Usuário ou senha incorretos." e chama self.exibir_menu_login_falho().

Importante: O exibir_menu_login_falho deve retornar uma "ação" (ex: "TENTAR_NOVAMENTE" ou "IR_CADASTRO"). A recursão é resolvida aqui.

exibir_menu_login_falho(self) -> str:

Lógica: Contém o while True de tratar_login_falho().

Se o usuário escolher 1, return "TENTAR_NOVAMENTE".

Se o usuário escolher 2, usuario_obj = self.executar_cadastro(). Se o cadastro for bem-sucedido, return usuario_obj (para logar direto).

executar_cadastro(self) -> Usuario | None:

Lógica: Contém todos os loops while de sistema_cadastro() para pedir dados.

Chama resultado = self.servico_auth.cadastrar_usuario(...).

Se isinstance(resultado, Usuario) (ou seja, se for um objeto Usuario), imprime "Conta criada!" e return resultado.

Se isinstance(resultado, str) (ou seja, se for uma mensagem de erro), imprime o erro e o loop de cadastro continua.

## Arquivo Atual: usuario_auth.py (Sugestão de novo nome)
Este arquivo será o "coração" da sua autenticação.

Tarefa 1: Corrigir e Completar a Classe Usuario (O Modelo)
Você está 95% lá. Vamos apenas corrigir um pequeno bug e adicionar os atributos que faltam (cadeiras, xp, etc.) para que a classe Usuario seja a única fonte de verdade sobre o usuário.

Classe: Usuario (Refatoração)

Atributos (Dados):

self.usuario: str

self.senha: str

self.instituicao: str

self.periodo: int

self.cadeiras: list (O mais importante: para guardar os objetos Cadeira)

self.xp: int

self.nivel: int

Métodos (Funções):

__init__(self, usuario, senha, instituicao, periodo, cadeiras=None, xp=0, nivel=1):

Ação: Atualize o construtor para receber os novos dados.

Lógica: self.cadeiras = cadeiras if cadeiras is not None else [] (Sempre inicialize listas assim).

senha_valida(self, entrada_senha):

Ação: Perfeito, mantenha como está.

to_dict(self): (Vamos renomear dicionario para to_dict por convenção)

Ação: Atualize este método para incluir os novos dados (cadeiras, xp, nivel).

Lógica: Você precisará converter a lista de objetos Cadeira de volta para uma lista de dicionários [c.to_dict() for c in self.cadeiras].

Correção de Bug: Alinhe os nomes. Se no __init__ você usou self.periodo, aqui deve ser 'periodo_atual': self.periodo. E 'instituicao': self.instituicao (sem "ç").

@classmethod from_dict(cls, dados):

Ação: Atualize este método para carregar os novos dados (cadeiras, xp, nivel).

Lógica: Use .get() para carregar os novos dados de forma segura (ex: xp = dados.get('xp', 0)).

Lógica de Cadeira: Você precisará converter a lista de dicionários de cadeiras (vinda do JSON) em uma lista de objetos Cadeira (usando Cadeira.from_dict()).

Tarefa 2: Renomear e Refinar Autenticacao para RepositorioUsuario (O Repositório)
Sua classe Autenticacao é, na verdade, um Repositório. Ela só fala com o arquivo JSON. Vamos renomeá-la para refletir sua responsabilidade única (SRP).

Classe: RepositorioUsuario (Antiga Autenticacao)

Responsabilidade: A única classe que sabe como ler e escrever usuários no conta.json.

Atributos (Dados):

self.caminho_arquivo: str

Métodos (Funções):

__init__(self, caminho_arquivo="conta.json"): Construtor.

_carregar_objetos_usuario(self) -> dict[str, Usuario]: (Renomear _carregar_usuarios)

Ação: Mantenha a lógica como está (carrega o JSON, itera e usa Usuario.from_dict). Perfeito.

_salvar_objetos_usuario(self, todos_usuarios: dict[str, Usuario]): (Renomear _salvar_usuario)

Ação: Mantenha a lógica como está (recebe dicionário de objetos, itera e usa usuario.to_dict(), salva no JSON). Perfeito.

encontrar_usuario(self, nome_usuario: str) -> Usuario | None: (Novo Método)

Lógica:

todos_usuarios = self._carregar_objetos_usuario()

return todos_usuarios.get(nome_usuario.lower())

salvar_usuario(self, usuario: Usuario): (Novo Método)

Lógica:

todos_usuarios = self._carregar_objetos_usuario()

todos_usuarios[usuario.usuario] = usuario

self._salvar_objetos_usuario(todos_usuarios)

Arquivo: servico_auth.py (Novo Arquivo - A "Lógica de Negócio")
Esta é a classe que vai substituir a lógica de validação do seu cadastro.py antigo. Ela é o "cérebro" que toma decisões.

Tarefa 3: Criar a Classe ServicoAutenticacao
Classe: ServicoAutenticacao

Responsabilidade: Orquestrar o login e o cadastro, aplicando as regras de negócio.

Atributos (Dados):

repositorio: RepositorioUsuario

Métodos (Funções):

__init__(self, repositorio: RepositorioUsuario): Construtor que recebe o repositório.

login(self, nome_usuario: str, senha_digitada: str) -> Usuario | None:

Lógica:

usuario_obj = self.repositorio.encontrar_usuario(nome_usuario)

if usuario_obj and usuario_obj.senha_valida(senha_digitada):

return usuario_obj

return None

cadastrar_usuario(self, nome, senha, instituicao, periodo) -> Usuario | str:

Responsabilidade: Aplicar as regras de negócio do seu cadastro.py antigo.

Lógica:

if not (0 < len(nome) <= 20): return "Erro: Nome de usuário inválido."

if not (0 < len(senha) <= 12): return "Erro: Senha inválida."

if self.repositorio.encontrar_usuario(nome): return "Erro: Usuário já existe."

if not (periodo.isdigit() and 0 < int(periodo) <= 15): return "Erro: Período inválido."

Se tudo passar:

novo_usuario = Usuario(nome, senha, instituicao, int(periodo))

self.repositorio.salvar_usuario(novo_usuario)

return novo_usuario (Retorna o objeto completo)

Arquivo: interface_auth.py (Novo Arquivo - A "Interface de Console")
Esta é a classe que substitui toda a interação com o usuário (print/input) do seu cadastro.py e login.py antigos.

Tarefa 4: Criar a Classe InterfaceAutenticacao
Classe: InterfaceAutenticacao

Responsabilidade: Exibir menus, pedir dados ao usuário e chamar o ServicoAutenticacao.

Atributos (Dados):

servico_auth: ServicoAutenticacao

Métodos (Funções):

__init__(self, servico: ServicoAutenticacao): Construtor.

executar_login(self) -> Usuario | None:

Lógica: Contém o while True de sistema_login().

Pede entrada_usuario e entrada_senha ao usuário.

Chama usuario_obj = self.servico_auth.login(entrada_usuario, entrada_senha).

Se usuario_obj: imprime "Logado!" e return usuario_obj.

Se None: imprime "Erro" e chama acao = self.exibir_menu_login_falho().

Se acao == "CADASTRO", chama return self.executar_cadastro().

Se acao == "TENTAR_NOVAMENTE", o loop continua (continue).

executar_cadastro(self) -> Usuario | None:

Lógica: Contém todos os while True de sistema_cadastro().

Pede criar_usuario, criar_senha, instituicao, periodo_entrada.

Chama resultado = self.servico_auth.cadastrar_usuario(...).

Se isinstance(resultado, Usuario) (sucesso): imprime "Conta criada!" e return resultado.

Se isinstance(resultado, str) (erro): imprime o resultado (a mensagem de erro) e o loop continua.

exibir_menu_login_falho(self) -> str:

Lógica: Pede ao usuário 1 ou 2 (try...except ValueError).

if escolha == 1: return "TENTAR_NOVAMENTE"

if escolha == 2: return "CADASTRO"

## Arquivos: interface_console.py e interface_horobot.py (Novos Arquivos)
Sua lógica de horobot.py será dividida em duas novas classes em dois novos arquivos. Esta é a refatoração mais "Pleno" que podemos fazer.

Tarefa 1: Criar a Classe InterfaceConsole (Novo Arquivo: interface_console.py)
Esta será a única classe em todo o seu projeto que terá permissão para usar print, input, os.system ou getpass. Ela centraliza toda a interação de I/O (Entrada/Saída) do terminal.

Classe: InterfaceConsole

Responsabilidade: Abstrair e controlar todo o I/O do console.

Atributos (Dados): (Nenhum por enquanto)

Métodos (Funções):

limpar_tela(self):

Lógica: os.system("cls" if os.name == "nt" else "clear")

exibir_mensagem(self, mensagem: str, autor="HOROBOT", delay_segundos=1):

Lógica: print(f"{autor}: {mensagem}"), time.sleep(delay_segundos)

exibir_arte(self, arte: str):

Lógica: print(arte) (Um método simples só para exibir a arte)

obter_input(self, prompt: str) -> str:

Lógica: return input(f"HOROBOT: {prompt}\nUsuario: ")

obter_senha(self, prompt: str) -> str:

Lógica: return getpass.getpass(f"HOROBOT: {prompt}\nSENHA: ")

pausar_tela(self, mensagem="\nPressione ENTER para continuar..."):

Lógica: input(mensagem)

Tarefa 2: Criar a Classe InterfaceHorobot (Novo Arquivo: interface_horobot.py)
Esta classe usa a InterfaceConsole para exibir as artes específicas do Horobot. Ela é a "dona" das artes ASCII.

Classe: InterfaceHorobot

Responsabilidade: Gerenciar e exibir todas as artes e mensagens padronizadas do Horobot.

Atributos (Dados):

console: InterfaceConsole (Ela precisa de um objeto InterfaceConsole para funcionar)

_APRESENTACAO = r"""...""" (Toda a arte ASCII do seu horobot.py vai aqui, como atributos privados, iniciados com _)

_CELEBRACAO = r"""..."""

_CONFUSO = r"""..."""

_PENSANDO = r"""..."""

_DORMINDO = r"""..."""

_NOVA_TAREFA = r"""..."""

Métodos (Funções):

__init__(self, console: InterfaceConsole):

Lógica: self.console = console (Isso se chama Injeção de Dependência)

exibir_apresentacao(self):

Lógica: self.console.limpar_tela(), self.console.exibir_arte(self._APRESENTACAO)

exibir_celebracao(self):

Lógica: self.console.limpar_tela(), self.console.exibir_arte(self._CELEBRACAO)

exibir_confuso(self):

Lógica: self.console.limpar_tela(), self.console.exibir_arte(self._CONFUSO)

exibir_pensando(self):

Lógica: self.console.limpar_tela(), self.console.exibir_arte(self._PENSANDO)

exibir_dormindo(self):

Lógica: self.console.limpar_tela(), self.console.exibir_arte(self._DORMINDO)

exibir_nova_tarefa(self):

Lógica: self.console.limpar_tela(), self.console.exibir_arte(self._NOVA_TAREFA)

Tarefas de Refatoração para as Outras Classes
Tarefa 3: Refatorar as Classes InterfaceAutenticacao e InterfaceCadeira
Agora que temos nossas novas classes de interface, as outras classes de Interface (que definimos nos passos anteriores) não podem mais usar print ou input diretamente. Elas devem usar a InterfaceConsole e a InterfaceHorobot.

Classe: InterfaceAutenticacao (Modificação)

Atributos (Dados):

servico_auth: ServicoAutenticacao

console: InterfaceConsole (Novo)

horobot: InterfaceHorobot (Novo)

Métodos (Funções):

__init__(self, servico_auth: ServicoAutenticacao, console: InterfaceConsole, horobot: InterfaceHorobot): O construtor agora recebe todas as suas dependências.

executar_login(self) -> Usuario | None:

Lógica Antiga: limpar_terminal(), print(...), input(...), getpass(...)

Lógica Nova (Exemplo):

self.console.limpar_tela()

entrada_usuario = self.console.obter_input("Digite seu nome de usuario:")

entrada_senha = self.console.obter_senha("Digite sua senha:")

usuario_obj = self.servico_auth.login(entrada_usuario, entrada_senha)

if usuario_obj: self.console.exibir_mensagem("Você agora esta logado!") ...

else: self.console.exibir_mensagem("Seu nome de usuario ou senha estão incorretos.") ...

Classe: InterfaceCadeira (Modificação)

Atributos (Dados):

servico_academico: ServicoAcademico

console: InterfaceConsole (Novo)

horobot: InterfaceHorobot (Novo)

Métodos (Funções):

__init__(self, servico_academico: ServicoAcademico, console: InterfaceConsole, horobot: InterfaceHorobot): Construtor atualizado.

exibir_menu_cadastrar_cadeira(self, usuario_logado):

Lógica Nova: Substituir todos os print por self.console.exibir_mensagem(...) e todos os input por self.console.obter_input(...).

## Arquivo: interface_menu.py (Novo Arquivo)
Vamos criar um novo arquivo para abrigar as classes de interface de menu. O Menu.py original será substituído.

Tarefa 1: Criar a Classe InterfaceMenuPrincipal
Esta classe vai substituir sua função menu_inicial. A responsabilidade dela é exibir o "dashboard" principal e encaminhar o usuário para os sub-menus.

Classe: InterfaceMenuPrincipal

Responsabilidade: Exibir o menu principal e gerenciar o fluxo de alto nível.

Atributos (Dados):

console: InterfaceConsole

horobot: InterfaceHorobot

repositorio_usuario: RepositorioUsuario

interface_academica: InterfaceAcademica (Esta é a classe que definiremos na Tarefa 2)

Métodos (Funções):

__init__(self, console, horobot, repositorio, interface_academica): O construtor para receber suas dependências (Injeção de Dependência).

_exibir_dashboard(self, usuario: Usuario):

Responsabilidade: Um método privado que substitui a parte visual do menu_inicial.

Lógica: Pega o objeto Usuario e usa self.console.exibir_mensagem(...) para imprimir os dados formatados (Nome, Nível, Universidade, barra de XP, etc.).

executar(self, usuario_logado: Usuario):

Responsabilidade: Substitui o while True da função menu_inicial.

Lógica:

Inicia o while True:.

self.console.limpar_tela().

usuario_atualizado = self.repositorio_usuario.encontrar_usuario(usuario_logado.usuario) (Carrega dados novos a cada loop).

self._exibir_dashboard(usuario_atualizado).

Usa self.console.obter_input(...) dentro de um try...except ValueError para pegar a escolha.

Usa if/elif para o Fluxo de Controle:

if escolha == 0: self.horobot.exibir_dormindo(); break (Não use quit(), apenas break para sair do loop e encerrar o programa).

elif escolha == 1: self.interface_academica.executar_menu_notas(usuario_atualizado)

elif escolha == 2: self.interface_academica.executar_menu_cadeiras(usuario_atualizado)

elif escolha in [3, 4, 5, 6]: self.horobot.exibir_confuso() (Ou uma arte de "em construção").

Tarefa 2: Criar a Classe InterfaceAcademica
Esta classe vai substituir ambas menu_notas e menu_cadeiras. É a interface unificada para toda a parte acadêmica.

Classe: InterfaceAcademica

Responsabilidade: Lidar com todas as interações de console para Notas e Cadeiras.

Atributos (Dados):

console: InterfaceConsole

horobot: InterfaceHorobot

servico_academico: ServicoAcademico (A classe que cadastra cadeiras/notas)

Métodos (Funções):

__init__(self, console, horobot, servico): Construtor.

executar_menu_notas(self, usuario: Usuario):

Responsabilidade: Substitui a função menu_notas.

Lógica:

Pega as cadeiras do objeto: lista_cadeiras = usuario.get_cadeiras().

Faz a checagem if not lista_cadeiras:.

Se não houver cadeiras, usa self.console para exibir o menu "1. Cadastrar" / "0. Voltar" e chama self.executar_menu_cadastrar_cadeira(usuario) se escolhido.

Se houver cadeiras, exibe o menu "1. Ver situação" / "2. Adicionar notas".

Se 1, chama self.executar_situacao_cadeiras(usuario).

Se 2, chama self.executar_menu_cadastrar_notas(usuario).

executar_menu_cadeiras(self, usuario: Usuario):

Responsabilidade: Substitui a função menu_cadeiras.

Lógica:

Pega lista_cadeiras = usuario.get_cadeiras().

Faz a checagem if not lista_cadeiras:.

Se houver, executa a lógica de 2 colunas (usando self.console.exibir_mensagem).

Exibe as opções (0, 100, 1-N).

Se 100, chama self.executar_menu_cadastrar_cadeira(usuario).

Se 1-N, chama self._exibir_detalhes_cadeira(lista_cadeiras[escolha - 1]).

_exibir_detalhes_cadeira(self, cadeira: Cadeira): (Método privado)

Responsabilidade: Substitui a lógica de exibir detalhes do menu_cadeiras antigo.

Lógica: Recebe um objeto Cadeira e usa self.console para imprimir seus atributos (cadeira.nome_cadeira, cadeira.get_notas_formatadas(), etc.).

executar_menu_cadastrar_cadeira(self, usuario: Usuario): (Já definido no Trello anterior, agora se encaixa aqui).

executar_menu_cadastrar_notas(self, usuario: Usuario): (Já definido no Trello anterior, agora se encaixa aqui).

executar_situacao_cadeiras(self, usuario: Usuario): (Já definido no Trello anterior, agora se encaixa aqui).

Tarefa 3: Criar a Classe InterfaceBoasVindas
Classe: InterfaceBoasVindas

Responsabilidade: Substituir a função boas_vindas_novo_usuario.

Atributos (Dados):

console: InterfaceConsole

Métodos (Funções):

__init__(self, console: InterfaceConsole): Construtor.

executar(self):

Lógica: Move toda a lógica de print e time.sleep da sua função boas_vindas_novo_usuario para cá, substituindo print por self.console.exibir_mensagem (sem autor e com delay).

## Arquivo: repositorio.py (Onde RepositorioUsuario vive)
A classe Dados é, na verdade, a funcionalidade central de um Repositório. Ela lida com o acesso aos dados. Vamos mover sua lógica para o RepositorioUsuario que definimos.

Tarefa 1: Absorver a Classe Dados no RepositorioUsuario
Classe: RepositorioUsuario (Modificação)

Responsabilidade: Esta classe já é dona do conta.json. A lógica de Dados pertence a ela.

Novos Métodos a Adicionar (Privados):

_carregar_json_bruto(self) -> dict:

Lógica: Mova toda a lógica da sua função Dados.carregar_conta para este novo método privado.

Refatoração "Pleno" (Importante): Remova todos os prints de dentro deste método. A camada de Repositório (Dados) nunca deve falar com o usuário. Se um erro acontecer, ela deve "levantar" (raise) uma exceção, e a camada de Interface irá capturá-la.

Lógica Corrigida:

Python

def _carregar_json_bruto(self):
    if not (os.path.exists(self.caminho_arquivo) and os.path.getsize(self.caminho_arquivo) > 0):
        return {}
    try:
        with open(self.caminho_arquivo, 'r', encoding='utf-8') as arq:
            return json.load(arq)
    except (json.JSONDecodeError, IOError) as e:
        # Relança a exceção para a camada de serviço/interface tratar
        raise Exception(f"Erro ao carregar {self.caminho_arquivo}: {e}")
_salvar_json_bruto(self, dados_dict: dict):

Lógica: Mova a lógica de Dados.salvar_conta para cá.

Refatoração "Pleno": Remova o print e adicione tratamento de erro.

Lógica Corrigida:

Python

def _salvar_json_bruto(self, dados_dict):
    try:
        with open(self.caminho_arquivo, 'w', encoding='utf-8') as arq:
            json.dump(dados_dict, arq, ensure_ascii=False, indent=4)
    except IOError as e:
        raise Exception(f"Erro ao salvar {self.caminho_arquivo}: {e}")
Métodos a Atualizar:

_carregar_objetos_usuario(self): (Da nossa refatoração anterior)

Lógica Antiga: conta = carregar_conta()

Lógica Nova: conta_bruta = self._carregar_json_bruto() (Chama seu próprio método)

_salvar_objetos_usuario(self, ...): (Da nossa refatoração anterior)

Lógica Antiga: salvar_conta(conta)

Lógica Nova: self._salvar_json_bruto(conta_dict) (Chama seu próprio método)

Arquivo: interface_console.py (Onde InterfaceConsole vive)
Esta classe é a nova casa para as funções genéricas de console da sua classe Utilitarios.

Tarefa 2: Absorver Utilitários Genéricos de Console
Classe: InterfaceConsole (Modificação)

Novos Métodos a Adicionar:

limpar_tela(self):

Lógica: Mova a lógica de Utilitarios.limpar_terminal para cá (sem o @staticmethod).

exibir_mensagem_espera(self, mensagem: str, segundos: int = 1):

Lógica: Mova a lógica de Utilitarios.exibir_mensagem_espera para cá (sem o @staticmethod), mas use seus próprios métodos:

self.exibir_mensagem(mensagem, autor="HOROBOT", delay_segundos=segundos)

Arquivo: interface_*.py (Interfaces Específicas)
As outras funções de Utilitarios são, na verdade, "Telas" ou "Interfaces" específicas. Elas pertencem às classes de Interface que já projetamos.

Tarefa 3: Mover pagina_em_construcao para InterfaceHorobot
Classe: InterfaceHorobot (Modificação)

Novo Método: exibir_em_construcao(self)

Lógica: Mova a lógica de Utilitarios.pagina_em_construcao para cá.

Refatoração: Substitua os prints e time.sleep por chamadas ao self.console:

Python

def exibir_em_construcao(self):
    self.console.limpar_tela()
    self.console.exibir_mensagem("Parabéns! Você acabou de acessar uma parte em desenvolvimento.", autor="DEVS", delay_segundos=0)
    self.console.exibir_mensagem("Mas a sua pagina desejada esta em outro castelo...", autor="DEVS", delay_segundos=0)
    self.console.exibir_mensagem("Esta funcionalidade será implementada em breve! O7", autor="DEVS", delay_segundos=0)
    self.console.exibir_mensagem_espera("Voltando ao menu em 3 segundos...", segundos=3)
Tarefa 4: Mover boas_vindas_menu para InterfaceMenuPrincipal
Classe: InterfaceMenuPrincipal (Modificação)

Novo Método: _exibir_boas_vindas_menu(self, nome_usuario: str) (Método privado)

Lógica: Mova a lógica de Utilitarios.boas_vindas_menu para cá e refatore para usar self.console.

Chamada: O método executar da InterfaceMenuPrincipal pode chamar self._exibir_boas_vindas_menu(usuario.usuario) logo após exibir o dashboard.

Tarefa 5: Mover exibir_cadeiras para InterfaceAcademica
Classe: InterfaceAcademica (Modificação)

Novo Método: _exibir_lista_cadeiras(self, usuario: Usuario) -> bool:

Responsabilidade: Substituir Utilitarios.exibir_cadeiras.

Lógica:

Recebe o objeto Usuario.

self.console.limpar_tela()

self.console.exibir_mensagem("Suas cadeiras cadastradas:\n", delay_segundos=0)

lista_cadeiras = usuario.get_cadeiras()

if not lista_cadeiras:

self.console.exibir_mensagem("Você não tem nenhuma cadeira cadastrada.", delay_segundos=2)

return False (Indica que não há cadeiras)

Loop: for i, cadeira in enumerate(lista_cadeiras):

self.console.exibir_mensagem(f"[{i + 1}] {cadeira.nome_cadeira} - Professor(a): {cadeira.nome_professor}", delay_segundos=0)

return True (Indica que há cadeiras)

## app.py (Refatorado)
Este arquivo terá duas novas partes:

Classe AplicacaoHorogo: A nova dona da lógica de fluxo de alto nível.

Função main(): A "fábrica" que constrói todas as nossas classes e as conecta.

Tarefa 1: Criar a Classe AplicacaoHorogo
Esta classe será o "maestro" da orquestra. Ela substitui a lógica do seu app.py atual.

Classe: AplicacaoHorogo

Responsabilidade: Gerenciar o ciclo de vida da aplicação (iniciar, autenticar, executar menu principal, desligar).

Atributos (Dados): (Ela recebe todas as suas "ferramentas" no construtor)

console: InterfaceConsole

horobot: InterfaceHorobot

interface_auth: InterfaceAutenticacao

menu_principal: InterfaceMenuPrincipal

Métodos (Funções):

__init__(self, console, horobot, interface_auth, menu_principal): Construtor para receber suas dependências.

_iniciar_autenticacao(self) -> Usuario | None: (Método privado)

Responsabilidade: Substituir o while True que pergunta "Já possui cadastro?".

Lógica:

while True:

try:

prompt = "\nAntes de mais nada, você já possui cadastro no HOROGO?\n1 - Sim \n2 - Não"

escolha = int(self.console.obter_input(prompt))

self.console.limpar_tela()

if escolha == 1:

self.console.exibir_mensagem("Perfeito! me passe as seguintes informações...")

return self.interface_auth.executar_login() (Chama a interface de login)

elif escolha == 2:

return self.interface_auth.executar_cadastro() (Chama a interface de cadastro)

else: self.console.exibir_mensagem("Opção inválida.")

except ValueError: self.console.exibir_mensagem("Digite apenas números.")

run(self):

Responsabilidade: O método principal que inicia o programa.

Lógica:

self.horobot.exibir_apresentacao()

self.console.exibir_mensagem_espera("É um prazer te receber aqui!")

self.console.exibir_mensagem_espera("Serei seu amigo e guia durante sua jornada academica!")

usuario_obj = self._iniciar_autenticacao() (Chama o método acima para obter o usuário logado)

if usuario_obj:

self.menu_principal.executar(usuario_obj) (Inicia o menu principal)

self.horobot.exibir_dormindo() (Substitui o print("Até a proxima"))

Tarefa 2: Criar a Nova Função main() (A "Fábrica")
Esta é a parte mais importante da arquitetura "Pleno". Esta função irá construir todos os objetos do seu sistema, conectando suas dependências.

Função: main() (Substitui sua main() atual)

Responsabilidade: Configurar e iniciar a aplicação (Injeção de Dependência).

Lógica:

Python

def main():
    # --- CAMADA 1: I/O (Console) ---
    # Primeiro, criamos as ferramentas de I/O
    console = InterfaceConsole()
    horobot = InterfaceHorobot(console)
    
    # --- CAMADA 2: DADOS (Repositório) ---
    # Criamos o objeto que sabe falar com o conta.json
    repo_usuario = RepositorioUsuario("conta.json")

    # --- CAMADA 3: LÓGICA (Serviços) ---
    # Criamos os "cérebros" que tomam decisões, dando a eles o repositório
    servico_auth = ServicoAutenticacao(repo_usuario)
    servico_academico = ServicoAcademico(repo_usuario) # (O serviço acadêmico também precisa do repositório para salvar)

    # --- CAMADA 4: INTERFACE (Views) ---
    # Criamos as interfaces que falam com o usuário, dando a elas o console e os serviços
    interface_auth = InterfaceAutenticacao(servico_auth, console)
    interface_academica = InterfaceAcademica(console, horobot, servico_academico)
    
    # Criamos o menu principal, que precisa das outras interfaces para funcionar
    menu_principal = InterfaceMenuPrincipal(console, horobot, repo_usuario, interface_academica)

    # --- CAMADA 5: APLICAÇÃO ---
    # Criamos a aplicação principal e damos a ela as interfaces de que precisa
    app = AplicacaoHorogo(console, horobot, interface_auth, menu_principal)
    
    # --- EXECUTAR ---
    app.run()
Tarefa 3: Atualizar os Imports
Seu app.py não importará mais funções, ele importará CLASSES.

Ação: Substitua todos os seus imports antigos por algo assim:

Python

# (Os nomes exatos dos arquivos e pastas dependem de como você os criou)
from HOROGO.Modulos.io.interface_console import InterfaceConsole
from HOROGO.Modulos.io.interface_horobot import InterfaceHorobot
from HOROGO.Modulos.auth.repositorio import RepositorioUsuario
from HOROGO.Modulos.auth.servico import ServicoAutenticacao
from HOROGO.Modulos.auth.interface import InterfaceAutenticacao
from HOROGO.Modulos.academico.servico import ServicoAcademico
from HOROGO.Modulos.academico.interface import InterfaceAcademica
from HOROGO.Modulos.menu.interface_menu import InterfaceMenuPrincipal

# A classe AplicacaoHorogo e a função main() podem viver no próprio app.py

