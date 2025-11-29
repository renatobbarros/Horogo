from typing import Any, Optional


class InterfaceMural:
    """Interface de mural com design limpo."""

    def __init__(self, console=None, servico_mural=None):
        self.console = console
        self.servico_mural = servico_mural

    def _print(self, texto: str):
        print(f"  {texto}")

    def _input(self, prompt: str) -> str:
        if self.console and hasattr(self.console, "obter_entrada"):
            try:
                return self.console.obter_entrada(prompt)
            except Exception:
                pass
        return input(f"\n  {prompt}\n  » ").strip()

    def cadastrar_evento(self):
        """Permite cadastrar um novo evento com validações."""
        if not self.servico_mural:
            self._print("Serviço de mural não configurado.")
            return

        if self.console and hasattr(self.console, "exibir_titulo"):
            self.console.exibir_titulo("Cadastrar Novo Evento")
        else:
            print("\n" + "━" * 60)
            print("  CADASTRAR NOVO EVENTO")
            print("━" * 60 + "\n")
        
        # exibir instruções
        print("  📝 Preencha os dados do evento:")
        print("  (Mínimo: título 3 chars, descrição 5 chars)")
        print("  (Data no formato: YYYY-MM-DD, ex: 2025-12-31)")
        print()

        titulo = self._input("Título do evento")
        data = self._input("Data (YYYY-MM-DD)")
        local = self._input("Local")
        descricao = self._input("Descrição")

        try:
            resultado = self.servico_mural.criar_evento(titulo, data, local, descricao)
            
            if isinstance(resultado, str):
                # retornou erro
                if self.console and hasattr(self.console, "exibir_erro"):
                    self.console.exibir_erro(resultado)
                else:
                    print(f"\n  ✗ {resultado}")
            else:
                # sucesso
                if self.console and hasattr(self.console, "exibir_sucesso"):
                    self.console.exibir_sucesso("Evento cadastrado com sucesso!")
                else:
                    print("\n  ✓ Evento cadastrado com sucesso!")
        except Exception as e:
            if self.console and hasattr(self.console, "exibir_erro"):
                self.console.exibir_erro(f"Erro ao cadastrar evento: {e}")
            else:
                print(f"\n  ✗ Erro ao cadastrar evento: {e}")

    def mostrar_eventos(self, usuario: Any):
        """Exibe lista de eventos futuros com design limpo."""
        if not self.servico_mural:
            self._print("Serviço de mural não configurado.")
            return

        try:
            eventos = self.servico_mural.listar_eventos_disponiveis()
        except Exception as e:
            if self.console and hasattr(self.console, "exibir_erro"):
                self.console.exibir_erro(f"Erro ao listar eventos: {e}")
            else:
                print(f"\n  ✗ Erro ao listar eventos: {e}")
            return

        if not eventos:
            if self.console and hasattr(self.console, "exibir_aviso"):
                self.console.exibir_aviso("Nenhum evento disponível no momento.")
            else:
                print("\n  ℹ Nenhum evento disponível no momento.\n")
            return

        if self.console and hasattr(self.console, "exibir_titulo"):
            self.console.exibir_titulo("Mural de Eventos")
        else:
            print("\n" + "━" * 60)
            print("  MURAL DE EVENTOS")
            print("━" * 60 + "\n")

        for i, evento in enumerate(eventos, 1):
            if hasattr(evento, "titulo"):
                print(f"\n  [{i}] {evento.titulo}")
                print(f"      📅 {evento.data}")
                print(f"      📍 {evento.local}")
                print(f"      📝 {evento.descricao}")
                print(f"      👥 {len(evento.participantes)} participante(s)")
            elif isinstance(evento, dict):
                print(f"\n  [{i}] {evento.get('titulo', 'Sem título')}")
                print(f"      📅 {evento.get('data', 'N/A')}")
                print(f"      📍 {evento.get('local', 'N/A')}")
                print(f"      📝 {evento.get('descricao', 'N/A')}")
                participantes = evento.get('participantes', [])
                print(f"      👥 {len(participantes)} participante(s)")

        print("\n" + "─" * 60 + "\n")

        resposta = input("  Deseja fazer check-in em algum evento? [S/N]\n  » ").strip().upper()
        if resposta != "S":
            return

        try:
            num = int(input("\n  Digite o número do evento\n  » ").strip())
            if not (1 <= num <= len(eventos)):
                if self.console and hasattr(self.console, "exibir_erro"):
                    self.console.exibir_erro("Número inválido")
                else:
                    print("\n  ✗ Número inválido.")
                return
        except Exception:
            if self.console and hasattr(self.console, "exibir_erro"):
                self.console.exibir_erro("Entrada inválida")
            else:
                print("\n  ✗ Entrada inválida.")
            return

        evento_escolhido = eventos[num - 1]
        
        if isinstance(usuario, dict):
            nome_usuario = usuario.get("usuario") or usuario.get("nome")
        else:
            nome_usuario = getattr(usuario, "usuario", getattr(usuario, "nome", None))

        if not nome_usuario:
            if self.console and hasattr(self.console, "exibir_erro"):
                self.console.exibir_erro("Não foi possível identificar o usuário")
            else:
                print("\n  ✗ Erro: não foi possível identificar o usuário.")
            return

        if hasattr(evento_escolhido, "titulo"):
            titulo_evento = evento_escolhido.titulo
        elif isinstance(evento_escolhido, dict):
            titulo_evento = evento_escolhido.get("titulo")
        else:
            if self.console and hasattr(self.console, "exibir_erro"):
                self.console.exibir_erro("Evento inválido")
            else:
                print("\n  ✗ Erro: evento inválido.")
            return

        try:
            ok = self.servico_mural.realizar_checkin(nome_usuario, titulo_evento)
            if ok:
                if self.console and hasattr(self.console, "exibir_sucesso"):
                    self.console.exibir_sucesso("Check-in realizado com sucesso!")
                else:
                    print("\n  ✓ Check-in realizado com sucesso!")
            else:
                if self.console and hasattr(self.console, "exibir_erro"):
                    self.console.exibir_erro("Falha ao realizar check-in")
                else:
                    print("\n  ✗ Falha ao realizar check-in.")
        except Exception as e:
            if self.console and hasattr(self.console, "exibir_erro"):
                self.console.exibir_erro(f"Erro ao realizar check-in: {e}")
            else:
                print(f"\n  ✗ Erro ao realizar check-in: {e}")

    def executar_menu_mural(self, usuario):
        """Menu completo do mural."""
        while True:
            if self.console and hasattr(self.console, "limpar_tela"):
                try:
                    self.console.limpar_tela()
                except Exception:
                    pass

            if self.console and hasattr(self.console, "exibir_titulo"):
                self.console.exibir_titulo("Mural")
            else:
                print("\n" + "━" * 60)
                print("  MURAL")
                print("━" * 60)

            print()
            print("  [1] Ver eventos disponíveis")
            print("  [2] Cadastrar novo evento")
            print("  [0] Voltar")
            print()
            
            opt = input("  » ").strip()
            
            if opt == "0":
                break
            elif opt == "1":
                self.mostrar_eventos(usuario)
                if self.console and hasattr(self.console, "pausar"):
                    self.console.pausar()
                else:
                    input("\n  Pressione ENTER para continuar...")
            elif opt == "2":
                self.cadastrar_evento()
                if self.console and hasattr(self.console, "pausar"):
                    self.console.pausar()
                else:
                    input("\n  Pressione ENTER para continuar...")
            else:
                if self.console and hasattr(self.console, "exibir_erro"):
                    self.console.exibir_erro("Opção inválida")
                else:
                    print("\n  ✗ Opção inválida.")