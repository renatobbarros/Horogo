class Nota:
    def __init__(self, va1, va2, va3, recuperacao):
        self.va1 = va1
        self.va2 = va2
        self.va3 = va3
        self.recuperacao = recuperacao
    
    def calcular_media_parcial(self):
        '''Calcula a média parcial considerando as regras de substituição'''
        if va1 != 0 and va2 != 0:
            media_parcial = (va1 + va2)/2
        elif va1 == None and va2 > 0:
            media_parcial = (va2 + va3)/2
        else:
            media_parcial = (va1 + va3)/2
        return media_parcial
    def calcular_media_final(self):
        '''Calcula a média final considerando a recuperação'''
        media_parcial = self.calcular_media_parcial()
        if self.recuperacao != None:
            media_final = (media_parcial + self.recuperacao)/2
        else:
            media_final = media_parcial
        return media_final
    def get_situacao(self):
        '''Retorna a situação do aluno com base na média final'''
        media_final = self.calcular_media_final()
        if media_final >= 7:
            return "Aprovado"
        else:
            return "Reprovado"
    def to_dict(self):
        '''Retorna um dicionário com as notas e a situação do aluno'''
        return {
            # pega todos os valores e adiciona ao dicionário
            "va1": self.va1,
            "va2": self.va2,
            "va3": self.va3,
            "recuperacao": self.recuperacao,
            "media_parcial": self.calcular_media_parcial(),
            "media_final": self.calcular_media_final(),
            "situacao": self.get_situacao()
        }


        

