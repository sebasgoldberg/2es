#!/usr/bin/python
#encoding=utf8

from els.utils import MappingFileGenerator
from els.lang import Lang

L = Lang.get_instance()

venda = MappingFileGenerator()
venda.add(L.loja)
venda.add(L.secao)
venda.add(L.custo)
venda.add(L.material)
venda.add(L.venda_liquida)
venda.add(L.matid)
venda.add(L.descricao_material)
venda.add(L.venda_bruta)
venda.add(L.quantidade)
venda.add(L.descricao_secao)
venda.add(L.data)

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

