
#!/usr/bin/python
#encoding=utf8

from els.utils import MappingFileGenerator
from els.lang import Lang
L = Lang.get_instance()

class RetailMapping(MappingFileGenerator):

    def __init__(self, *args, **kwargs):

        MappingFileGenerator.__init__(self, *args, **kwargs)
        self.add(L.loja)
        self.add(L.secao)
        self.add(L.descricao_secao)
        self.add(L.material)
        self.add(L.descricao_material)
        self.add(L.matid)

        self.add(L.data)

        # venda
        self.add(L.venda_bruta)
        self.add(L.venda_liquida)
        self.add(L.custo)
        self.add(L.quantidade_vendida)

        # ruptura
        self.add(L.ruptura)
        self.add(L.perda)

        # quebra
        self.add(L.importe_quebra)



