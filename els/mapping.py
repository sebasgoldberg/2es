#!/usr/bin/python
#encoding=utf8

from els.utils import MappingFileGenerator
from els.lang import Lang

L = Lang.get_instance()

wdecide = MappingFileGenerator()
wdecide.add(L.option)
wdecide.add(L.criteria)
wdecide.save('./wdecide/mapping.json')


venda = MappingFileGenerator()
venda.add(L.loja)
venda.add(L.secao)
venda.add(L.material)
venda.add(L.matid)
venda.add(L.descricao_material)
venda.add(L.descricao_secao)

venda.add(L.venda_bruta)
venda.add(L.quantidade)
venda.add(L.custo)
venda.add(L.venda_liquida)

venda.save('./venda/mapping.json')


ruptura = MappingFileGenerator()
ruptura.add(L.loja)
ruptura.add(L.secao)
ruptura.add(L.material)
ruptura.add(L.matid)
ruptura.add(L.descricao_material)
ruptura.add(L.descricao_secao)
ruptura.add(L.data)
ruptura.add(L.ruptura)
ruptura.add(L.perda)

ruptura.save('./ruptura/mapping.json')


precios = MappingFileGenerator()
precios.add(L.loja)
precios.add(L.secao)
precios.add(L.material)
precios.add(L.matid)
precios.add(L.matid_com_um)
precios.add(L.descricao_material)
precios.add(L.descricao_secao)
precios.add(L.data)
precios.add(L.matid)
precios.add(L.rankvarabs)
precios.add(L.rankvartot)
precios.add(L.media)
precios.add(L.desvio)
precios.add(L.indice_variacion)

precios.save('./precios/mapping.json')

quebra = MappingFileGenerator()
quebra.add(L.matid)
quebra.add(L.loja)
quebra.add(L.secao)
quebra.add(L.descricao_secao)
quebra.add(L.material)
quebra.add(L.descricao_material)
quebra.add(L.unidade_medida)
quebra.add(L.tipo_movimento)
quebra.add(L.quantidade)
quebra.add(L.data)
quebra.add(L.importe)

quebra.save('./quebra/mapping.json')



windows_clients = MappingFileGenerator()
windows_clients.add(L.estado_antivirus)
windows_clients.add(L.nome_maquina)
windows_clients.add(L.auto_gestao_senha)
windows_clients.add(L.lync)
windows_clients.add(L.data)
windows_clients.add(L.altiris)
windows_clients.add(L.osArch)
windows_clients.add(L.osVersion)
windows_clients.add(L.status)
windows_clients.add(L.ip)
windows_clients.add(L.local)
windows_clients.add(L.pcA)
windows_clients.save('./mac/mapping.json')



from retail.mapping import RetailMapping
retail = RetailMapping()
retail.save('./retail/mapping.json')


