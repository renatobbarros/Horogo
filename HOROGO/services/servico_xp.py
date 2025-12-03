from typing import Dict, List, Tuple, Any
from ..repository.repositorio_usuario import repositorio_usuario


class ServicoXP:
    """onde tudo de XP e gerenciado, adicionar XP, calcular nivel, etc."""
    XP_POR_NIVEL = {
        1: 0, 2: 100, 3: 250, 4: 450, 5: 700,
        6: 1000, 7: 1350, 8: 1750, 9: 2200, 10: 2700,
        11: 3250, 12: 3850, 13: 4500, 14: 5200, 15: 6000,
    }

    TITULOS = {
        1: "Calouro", 2: "Estudante", 3: "Aplicado",
        4: "Dedicado", 5: "Veterano", 6: "Experiente",
        7: "Mestre", 8: "Sábio", 9: "Guru",
        10: "Lenda", 11: "Ícone", 12: "Herói",
        13: "Campeão", 14: "Mito", 15: "Deus do Campus",
    }

    XP_ACOES = {
        "cadastro": 50,
        "login_diario": 10,
        "cadastrar_cadeira": 20,
        "atualizar_notas": 30,
        "checkin_evento": 15,
        "criar_evento": 25,
        "completar_perfil": 40,
    }

    def __init__(self, repositorio: repositorio_usuario):
        self.repositorio = repositorio

    def calcular_nivel(self, xp: int) -> int:
        nivel = 1
        for n, xp_necessario in sorted(self.XP_POR_NIVEL.items()):
            if xp >= xp_necessario:
                nivel = n
            else:
                break
        return nivel

    def xp_para_proximo_nivel(self, xp_atual: int) -> int:
        nivel_atual = self.calcular_nivel(xp_atual)
        if nivel_atual >= 15:
            return 0
        xp_necessario = self.XP_POR_NIVEL.get(nivel_atual + 1, 0)
        return xp_necessario - xp_atual

    def obter_titulo(self, nivel: int) -> str:
        return self.TITULOS.get(nivel, "Desconhecido")

    def adicionar_xp(self, nome_usuario: str, acao: str, quantidade: int = None) -> Tuple[bool, str, Dict]:
        usuario = self.repositorio.encontrar_usuario(nome_usuario)
        if not usuario:
            return False, "Usuário não encontrado", {}

        if quantidade is not None:
            xp_ganho = int(quantidade)
        else:
            xp_ganho = self.XP_ACOES.get(acao, 0)

        if xp_ganho <= 0:
            return False, "Ação inválida ou XP zero", {}

        xp_anterior = getattr(usuario, "xp", 0)
        nivel_anterior = self.calcular_nivel(xp_anterior)

        xp_novo = xp_anterior + xp_ganho
        nivel_novo = self.calcular_nivel(xp_novo)

        usuario.xp = xp_novo
        usuario.nivel = nivel_novo

        try:
            self.repositorio.salvar_usuario(usuario)
        except Exception as e:
            return False, f"Erro ao salvar: {e}", {}

        subiu_nivel = nivel_novo > nivel_anterior

        info = {
            "xp_ganho": xp_ganho,
            "xp_total": xp_novo,
            "nivel_anterior": nivel_anterior,
            "nivel_novo": nivel_novo,
            "subiu_nivel": subiu_nivel,
            "titulo_novo": self.obter_titulo(nivel_novo) if subiu_nivel else None,
        }

        if subiu_nivel:
            msg = f"🎉 Parabéns! Você subiu para o nível {nivel_novo} - {self.obter_titulo(nivel_novo)}!"
        else:
            msg = f"✓ +{xp_ganho} XP ganho!"

        return True, msg, info

    def obter_estatisticas(self, nome_usuario: str) -> Dict[str, Any]:
        usuario = self.repositorio.encontrar_usuario(nome_usuario)
        if not usuario:
            return {}

        xp = getattr(usuario, "xp", 0)
        nivel = self.calcular_nivel(xp)
        xp_faltando = self.xp_para_proximo_nivel(xp)
        titulo = self.obter_titulo(nivel)
        xp_nivel_atual = self.XP_POR_NIVEL.get(nivel, 0)
        xp_proximo_nivel = self.XP_POR_NIVEL.get(nivel + 1, xp + 1)
        progresso = xp - xp_nivel_atual
        progresso_total = xp_proximo_nivel - xp_nivel_atual

        return {
            "xp": xp,
            "nivel": nivel,
            "titulo": titulo,
            "xp_faltando": xp_faltando,
            "xp_nivel_atual": xp_nivel_atual,
            "xp_proximo_nivel": xp_proximo_nivel,
            "progresso": progresso,
            "progresso_total": progresso_total,
            "percentual": int((progresso / progresso_total) * 100) if progresso_total > 0 else 100,
        }

    def listar_acoes_disponiveis(self) -> List[Tuple[str, int]]:
        return [(acao, xp) for acao, xp in self.XP_ACOES.items()]