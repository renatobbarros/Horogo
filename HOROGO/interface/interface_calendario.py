from typing import Any


class InterfaceCalendario:
    def __init__(self, servico_calendario: Any, console: Any, repositorio=None):
        self.servico = servico_calendario
        self.console = console
        self.repo = repositorio  # usado para salvar xp no usuario

    def executar(self, usuario):
        # menu simples do calendário
        while True:
            try:
                if hasattr(self.console, "limpar_tela"):
                    try:
                        self.console.limpar_tela()
                    except Exception:
                        pass
                self.console.exibir_titulo("CALENDÁRIO") if hasattr(self.console, "exibir_titulo") else None
                self.console.exibir_mensagem("1 - Ver tarefas\n2 - Cadastrar tarefa\n3 - Cadastrar data importante\n4 - Ver datas importantes\n0 - Voltar")
                escolha = self.console.obter_entrada("Escolha:")
                if escolha == "1":
                    self._listar_tarefas(usuario)
                elif escolha == "2":
                    self._cadastrar_tarefa()
                elif escolha == "3":
                    self._cadastrar_data()
                elif escolha == "4":
                    self._listar_datas(usuario)
                elif escolha == "0":
                    break
                else:
                    self.console.exibir_mensagem("Opção inválida.")
                try:
                    self.console.pausar()
                except Exception:
                    pass
            except Exception as e:
                try:
                    self.console.exibir_erro(f"Erro no calendário: {e}")
                    try:
                        self.console.pausar()
                    except Exception:
                        pass
                except Exception:
                    pass
                break

    def _listar_tarefas(self, usuario):
        tarefas = self.servico.listar_tarefas()
        if not tarefas:
            self.console.exibir_mensagem("Nenhuma tarefa cadastrada.")
            return
        for i, t in enumerate(tarefas):
            tempo = t.tempo_restante()
            self.console.exibir_mensagem(f"{i+1}. [ ] {t.titulo} ({t.tipo}) - {t.data_iso} - falta: {tempo} - XP: {t.xp}")

        escolha = self.console.obter_entrada("Marcar tarefa como concluída? (número ou 0 para voltar)")
        try:
            n = int(escolha)
        except Exception:
            return
        if n <= 0:
            return
        xp = self.servico.marcar_tarefa_concluida(n - 1)
        if xp and usuario:
            try:
                usuario.xp = getattr(usuario, "xp", 0) + int(xp)
                if self.repo:
                    try:
                        self.repo.salvar_usuario(usuario)
                    except Exception:
                        pass
                self.console.exibir_sucesso(f"Tarefa concluída! Você ganhou {xp} XP.")
            except Exception:
                pass

    def _cadastrar_tarefa(self):
        titulo = self.console.obter_entrada("Título da tarefa")
        tipo = self.console.obter_entrada("Tipo (trabalho/atividade/palestra)")
        data = self.console.obter_entrada("Data (YYYY-MM-DD ou YYYY-MM-DDTHH:MM)")
        try:
            xp = int(self.console.obter_entrada("XP (opcional, enter para padrão)"))
        except Exception:
            xp = None
        self.servico.adicionar_tarefa(titulo, tipo, data, xp)
        self.console.exibir_sucesso("Tarefa cadastrada com sucesso!")

    def _cadastrar_data(self):
        nome = self.console.obter_entrada("Nome da data importante")
        data = self.console.obter_entrada("Data (YYYY-MM-DD)")
        try:
            xp = int(self.console.obter_entrada("XP (opcional, enter para padrão)"))
        except Exception:
            xp = 10
        self.servico.adicionar_data_importante(nome, data, xp)
        self.console.exibir_sucesso("Data importante cadastrada!")

    def _listar_datas(self, usuario):
        datas = self.servico.listar_datas_importantes()
        if not datas:
            self.console.exibir_mensagem("Nenhuma data importante cadastrada.")
            return
        for i, d in enumerate(datas):
            tempo = d.tempo_restante()
            self.console.exibir_mensagem(f"{i+1}. [ ] {d.nome} - {d.data_iso} - falta: {tempo} - XP: {d.xp}")

        escolha = self.console.obter_entrada("Marcar data como concluída? (número ou 0 para voltar)")
        try:
            n = int(escolha)
        except Exception:
            return
        if n <= 0:
            return
        xp = self.servico.marcar_data_concluida(n - 1)
        if xp and usuario:
            try:
                usuario.xp = getattr(usuario, "xp", 0) + int(xp)
                if self.repo:
                    try:
                        self.repo.salvar_usuario(usuario)
                    except Exception:
                        pass
                self.console.exibir_sucesso(f"Data marcada! Você ganhou {xp} XP.")
            except Exception:
                pass
