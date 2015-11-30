#!/usr/bin/python
#encoding=utf8

class Lang:

    instance = None

    @staticmethod
    def get_instance():
        
        if Lang.instance is None:
            Lang.instance = Lang()
        
        return Lang.instance

    def __init__(self):

        self.material = 'material'
        self.loja = 'loja'
        self.data = 'data'
        self.preco = 'preco'
        self.matid_com_um = 'matid_com_um'
        self.matid = 'matid'
        self.unidade_medida = 'unidade_medida'
        self.descricao_material = 'descricao_material'
        self.tipo_condicao = 'tipo_condicao'
        #self.fornecedor = 'fornecedor'
        self.secao = 'secao'
        self.descricao_secao = 'descricao_secao'
        self.tipo_movimento = 'tipo_movimento'

        self.venda_bruta = "venda_bruta"
        self.venda_liquida = "venda_liquida"
        self.quantidade = "quantidade"
        self.custo = "custo"
        self.perda = "perda"
        self.ruptura = "ruptura"
        self.rankvarabs = "rankvarabs"
        self.rankvartot = "rankvartot"
        self.media = 'media'
        self.desvio = 'desvio'
        self.indice_variacion = 'indice_variacion'
        self.importe = 'importe'

        self.estado_antivirus = "estado_antivirus"
        self.nome_maquina = "nome_maquina"
        self.auto_gestao_senha = "auto_gestao_senha"
        self.lync = "lync"
        self.altiris = "altiris"
        self.osArch = "osArch"
        self.osVersion = "osVersion"
        self.status = "status"
        self.ip = "ip"
        self.local = "local"
        self.pcA = "pcA"

        self.quantidade_vendida = "quantidade_vendida"
        self.quantidade_quebra = "quantidade_quebra"
        self.importe_quebra = "importe_quebra"

        self.types = {}
        self.types[self.material] = 'string'
        self.types[self.loja] = 'string'
        self.types[self.data] = 'date'
        self.types[self.preco] = 'double'
        self.types[self.matid_com_um] = 'string'
        self.types[self.matid] = 'string'
        self.types[self.unidade_medida] = 'string'
        self.types[self.descricao_material] = 'string'
        self.types[self.tipo_condicao] = 'string'
        self.types[self.secao] = 'string'
        self.types[self.descricao_secao] = 'string'
        self.types[self.tipo_movimento] = 'string'

        self.types[self.venda_bruta] = "double"
        self.types[self.venda_liquida] = "double"
        self.types[self.quantidade] = "double"
        self.types[self.custo] = "double"
        self.types[self.perda] = "double"
        self.types[self.ruptura] = "short"

        self.types[self.rankvarabs] = "double"
        self.types[self.rankvartot] = "double"
        self.types[self.media] = 'double'
        self.types[self.desvio] = 'double'
        self.types[self.indice_variacion] = 'double'
        self.types[self.importe] = 'double'

        self.types[self.estado_antivirus] = "short"
        self.types[self.nome_maquina] = "string"
        self.types[self.auto_gestao_senha] = "short"
        self.types[self.lync] = "short"
        self.types[self.altiris] = "short"
        self.types[self.osArch] = "string"
        self.types[self.osVersion] = "string"
        self.types[self.status] = "short"
        self.types[self.ip] = "ip"
        self.types[self.local] = "string"
        self.types[self.pcA] = "short"

        self.types[self.quantidade_vendida] = "double"
        self.types[self.quantidade_quebra] = "double"
        self.types[self.importe_quebra] = "double"

    def get_fieldtype(self, field):
        return self.types[field]

