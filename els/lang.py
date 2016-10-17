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

        self.option = "option"
        self.criteria = "criteria"

        self.mail = "mail"
        self.msExchRecipientTypeDetails  = "msExchRecipientTypeDetails" 
        self.cn = "cn"
        self.sAMAccountName = "sAMAccountName"
        self.bandeira = "bandeira"
        self.regional = "regional"
        self.loja_critica = "loja_critica"
        self.tipo_loja = "tipo_loja"
        self.lat_lon = "lat_lon"

        self.nota = 'nota'
        self.serie = 'serie'
        self.cnpj = 'cnpj'
        self.pedido = 'pedido'
        self.fornecedor = 'fornecedor'
        self.data_emissao = 'data_emissao'
        self.data_criacao = 'data_criacao'
        self.total_produto = 'total_produto'
        self.total_nota = 'total_nota'
        self.enviada_sap = 'enviada_sap'
        self.centro = 'centro'
        self.tipo_centro = 'tipo_centro'
        self.org_venda = 'org_venda'
        self.erro_remessa = 'erro_remessa'
        self.erro_cadastro = 'erro_cadastro'
        self.erro_comercial = 'erro_comercial'
        self.erro_custo_real = 'erro_custo_real'
        self.erro_embalagem = 'erro_embalagem'
        self.erro_fiscal = 'erro_fiscal'
        self.erro_material = 'erro_material'
        self.erro_quantidade = 'erro_quantidade'
        self.erro_operacional = 'erro_operacional'
        self.erro_custo = 'erro_custo'
        self.nome_fantasia = 'nome_fantasia'
        self.dia = 'dia'
        self.mes = 'mes'
        self.semana = 'semana'
        self.check_nfs = 'check_nfs'
        self.check_pedido = 'check_pedido'
        self.consolidado_supply = 'consolidado_supply'
        self.horti = 'horti'
        self.tipo_erro = 'tipo_erro'
        self.quan_erros = 'quan_erros'

        self.pais = 'pais'
        self.visao = 'visao'
        self.conceito = 'conceito'
        self.item = 'item'
        self.evaluacao = 'evaluacao'
        self.benchmark = 'benchmark'
        self.ano = 'ano'

        self.estabelecimento = 'estabelecimento'
        self.matricula = 'matricula'
        self.nome = 'nome'
        self.cargo = 'cargo'
        self.diretoria = 'diretoria'
        self.unidad_lotacao = 'unidad_lotacao'
        self.perfil = 'perfil'
        self.faixa_etaria = 'faixa_etaria'
        self.sexo = 'sexo'
        self.tempo_casa = 'tempo_casa'
        self.uf_trab = 'uf_trab'
        self.localidade = 'localidade'
        self.admissao = 'admissao'
        self.nascimento = 'nascimento'

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

        self.types[self.option] = "string"
        self.types[self.criteria] = "string"

        self.types[self.mail] = "string"
        self.types[self.msExchRecipientTypeDetails]  = "long" 
        self.types[self.cn] = "string"
        self.types[self.sAMAccountName] = "string"

        self.types[self.bandeira] = "string"
        self.types[self.regional] = "string"
        self.types[self.loja_critica] = "short"
        self.types[self.tipo_loja] = "string"
        self.types[self.lat_lon] = "geo_point"

        self.types[self.nota] = 'string'
        self.types[self.serie] = 'string'
        self.types[self.cnpj] = 'string'
        self.types[self.pedido] = 'string'
        self.types[self.fornecedor] = 'string'
        self.types[self.data_emissao] = 'date'
        self.types[self.data_criacao] = 'date'
        self.types[self.total_produto] = 'double'
        self.types[self.total_nota] = 'double'
        self.types[self.enviada_sap] = 'string'
        self.types[self.centro] = 'string'
        self.types[self.tipo_centro] = 'string'
        self.types[self.org_venda] = 'string'
        self.types[self.erro_remessa] = 'short'
        self.types[self.erro_cadastro] = 'short'
        self.types[self.erro_comercial] = 'short'
        self.types[self.erro_custo_real] = 'short'
        self.types[self.erro_embalagem] = 'short'
        self.types[self.erro_fiscal] = 'short'
        self.types[self.erro_material] = 'short'
        self.types[self.erro_quantidade] = 'short'
        self.types[self.erro_operacional] = 'short'
        self.types[self.erro_custo] = 'short'
        self.types[self.nome_fantasia] = 'string'
        self.types[self.dia] = 'short'
        self.types[self.mes] = 'short'
        self.types[self.semana] = 'string'
        self.types[self.check_nfs] = 'string'
        self.types[self.check_pedido] = 'string'
        self.types[self.consolidado_supply] = 'short'
        self.types[self.horti] = 'string'
        self.types[self.tipo_erro] = 'string'
        self.types[self.quan_erros] = 'short'

        self.types[self.pais] = 'string'
        self.types[self.visao] = 'string'
        self.types[self.conceito] = 'string'
        self.types[self.item] = 'string'
        self.types[self.evaluacao] = 'double'
        self.types[self.benchmark] = 'double'
        self.types[self.ano] = 'long'

        self.types[self.estabelecimento] = 'string'
        self.types[self.matricula] = 'string'
        self.types[self.nome] = 'string'
        self.types[self.cargo] = 'string'
        self.types[self.diretoria] = 'string'
        self.types[self.unidad_lotacao] = 'string'
        self.types[self.perfil] = 'string'
        self.types[self.faixa_etaria] = 'string'
        self.types[self.sexo] = 'string'
        self.types[self.tempo_casa] = 'string'
        self.types[self.uf_trab] = 'string'
        self.types[self.localidade] = 'string'
        self.types[self.admissao] = 'date'
        self.types[self.nascimento] = 'date'
        self.types['GPTW'] = {
            'ano': 'short',
            'visao': 'string',
            'dimensao': 'string',
            'num_item': 'short',
            'item': 'string',
            'avaliacao': 'short',
            }

    def get_fieldtype(self, field):
        return self.types[field]

