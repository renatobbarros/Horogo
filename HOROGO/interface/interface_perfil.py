from typing import Any


class InterfacePerfil:
    def __init__(self, console=None, servico_perfil=None):
        self.console = console
        self.servico_perfil = servico_perfil

    def _print(self, texto: str):
        print(f"  {texto}")

    def _input(self, prompt: str) -> str:
        if self.console and hasattr(self.console, "obter_entrada"):
            try:
                return self.console.obter_entrada(prompt)
            except Exception:
                pass
        return input(f"\n  {prompt}\n  » ").strip()

    def _exibir_dados(self, usuario: Any):
        """Exibe os dados do perfil do usuário."""
        if self.console and hasattr(self.console, "exibir_titulo"):
            self.console.exibir_titulo("Meu Perfil")
        else:
            print("\n" + "━" * 60)
            print("  MEU PERFIL")
            print("━" * 60 + "\n")

        # normalizar dados
        if isinstance(usuario, dict):
            nome = usuario.get("usuario") or usuario.get("nome", "N/A")
            instituicao = usuario.get("instituicao", "N/A")
            periodo = usuario.get("periodo", "N/A")
            xp = usuario.get("xp", 0)
            nivel = usuario.get("nivel", 1)
        else:
            nome = getattr(usuario, "usuario", getattr(usuario, "nome", "N/A"))
            instituicao = getattr(usuario, "instituicao", "N/A")
            periodo = getattr(usuario, "periodo", "N/A")
            xp = getattr(usuario, "xp", 0)
            nivel = getattr(usuario, "nivel", 1)

        print(f"  👤 Nome: {nome}")
        print(f"  🎓 Instituição: {instituicao}")
        print(f"  📚 Período: {periodo}")
        print(f"  ⭐ XP: {xp}")
        print(f"  🏆 Nível: {nivel}")
        print()

    def _menu_edicao(self, usuario: Any) -> bool:
        """
        Menu de edição do perfil.
        Retorna True se houve alteração, False caso contrário.
        """
        if not self.servico_perfil:
            self._print("Serviço de perfil não configurado.")
            return False

        if self.console and hasattr(self.console, "exibir_titulo"):
            self.console.exibir_titulo("Editar Perfil")
        else:
            print("\n" + "━" * 60)
            print("  EDITAR PERFIL")
            print("━" * 60 + "\n")

        print("  [1] Alterar senha")
        print("  [2] Alterar instituição")
        print("  [3] Alterar período")
        print("  [0] Voltar")
        print()

        opt = input("  » ").strip()

        # obter nome do usuario
        if isinstance(usuario, dict):
            nome_usuario = usuario.get("usuario") or usuario.get("nome")
        else:
            nome_usuario = getattr(usuario, "usuario", getattr(usuario, "nome", None))

        if not nome_usuario:
            if self.console and hasattr(self.console, "exibir_erro"):
                self.console.exibir_erro("Não foi possível identificar o usuário")
            else:
                self._print("✗ Erro: não foi possível identificar o usuário")
            return False

        if opt == "0":
            return False

        elif opt == "1":
            # alterar senha
            nova_senha = self._input("Digite a nova senha (4-12 caracteres)")
            confirmacao = self._input("Confirme a nova senha")

            if nova_senha != confirmacao:
                if self.console and hasattr(self.console, "exibir_erro"):
                    self.console.exibir_erro("As senhas não conferem")
                else:
                    self._print("✗ As senhas não conferem")
                return False

            try:
                resultado = self.servico_perfil.atualizar_senha(nome_usuario, nova_senha)
                if isinstance(resultado, str):
                    if self.console and hasattr(self.console, "exibir_erro"):
                        self.console.exibir_erro(resultado)
                    else:
                        self._print(f"✗ {resultado}")
                    return False
                else:
                    if self.console and hasattr(self.console, "exibir_sucesso"):
                        self.console.exibir_sucesso("Senha alterada com sucesso!")
                    else:
                        self._print("✓ Senha alterada com sucesso!")
                    # atualizar referência do usuario
                    if isinstance(usuario, dict):
                        usuario["senha"] = nova_senha
                    else:
                        usuario.senha = nova_senha
                    return True
            except Exception as e:
                if self.console and hasattr(self.console, "exibir_erro"):
                    self.console.exibir_erro(f"Erro ao alterar senha: {e}")
                else:
                    self._print(f"✗ Erro ao alterar senha: {e}")
                return False

        elif opt == "2":
            # alterar instituição
            nova_instituicao = self._input("Digite a nova instituição")

            try:
                resultado = self.servico_perfil.atualizar_instituicao(nome_usuario, nova_instituicao)
                if isinstance(resultado, str):
                    if self.console and hasattr(self.console, "exibir_erro"):
                        self.console.exibir_erro(resultado)
                    else:
                        self._print(f"✗ {resultado}")
                    return False
                else:
                    if self.console and hasattr(self.console, "exibir_sucesso"):
                        self.console.exibir_sucesso("Instituição alterada com sucesso!")
                    else:
                        self._print("✓ Instituição alterada com sucesso!")
                    # atualizar referência
                    if isinstance(usuario, dict):
                        usuario["instituicao"] = nova_instituicao
                    else:
                        usuario.instituicao = nova_instituicao
                    return True
            except Exception as e:
                if self.console and hasattr(self.console, "exibir_erro"):
                    self.console.exibir_erro(f"Erro ao alterar instituição: {e}")
                else:
                    self._print(f"✗ Erro ao alterar instituição: {e}")
                return False

        elif opt == "3":
            # alterar período
            novo_periodo = self._input("Digite o novo período (1-15)")

            try:
                resultado = self.servico_perfil.atualizar_periodo(nome_usuario, novo_periodo)
                if isinstance(resultado, str):
                    if self.console and hasattr(self.console, "exibir_erro"):
                        self.console.exibir_erro(resultado)
                    else:
                        self._print(f"✗ {resultado}")
                    return False
                else:
                    if self.console and hasattr(self.console, "exibir_sucesso"):
                        self.console.exibir_sucesso("Período alterado com sucesso!")
                    else:
                        self._print("✓ Período alterado com sucesso!")
                    # atualizar referência
                    if isinstance(usuario, dict):
                        usuario["periodo"] = int(novo_periodo)
                    else:
                        usuario.periodo = int(novo_periodo)
                    return True
            except Exception as e:
                if self.console and hasattr(self.console, "exibir_erro"):
                    self.console.exibir_erro(f"Erro ao alterar período: {e}")
                else:
                    self._print(f"✗ Erro ao alterar período: {e}")
                return False

        else:
            if self.console and hasattr(self.console, "exibir_erro"):
                self.console.exibir_erro("Opção inválida")
            else:
                self._print("✗ Opção inválida")
            return False

    def executar(self, usuario: Any):
        """Menu principal do perfil."""
        while True:
            if self.console and hasattr(self.console, "limpar_tela"):
                try:
                    self.console.limpar_tela()
                except Exception:
                    pass

            if self.console and hasattr(self.console, "exibir_titulo"):
                self.console.exibir_titulo("Perfil")
            else:
                print("\n" + "━" * 60)
                print("  PERFIL")
                print("━" * 60)

            print()
            print("  [1] Ver dados do perfil")
            print("  [2] Editar perfil")
            print("  [0] Voltar")
            print()

            opt = input("  » ").strip()

            if opt == "0":
                break
            elif opt == "1":
                self._exibir_dados(usuario)
                if self.console and hasattr(self.console, "pausar"):
                    self.console.pausar()
                else:
                    input("\n  Pressione ENTER para continuar...")
            elif opt == "2":
                alterado = self._menu_edicao(usuario)
                if alterado:
                    # recarregar dados do usuario após alteração
                    if isinstance(usuario, dict):
                        nome_usuario = usuario.get("usuario") or usuario.get("nome")
                    else:
                        nome_usuario = getattr(usuario, "usuario", getattr(usuario, "nome", None))
                    
                    # nota: em produção, você deveria recarregar o usuario do repositório
                    # mas como estamos alterando a referência diretamente, não é necessário aqui
                
                if self.console and hasattr(self.console, "pausar"):
                    self.console.pausar()
                else:
                    input("\n  Pressione ENTER para continuar...")
            else:
                if self.console and hasattr(self.console, "exibir_erro"):
                    self.console.exibir_erro("Opção inválida")
                else:
                    print("\n  ✗ Opção inválida")