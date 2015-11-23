#!/usr/bin/python
#encoding=utf8
__author__ = 'JSGold'

import datetime
import sys
import ntpath

FORNECEDOR = 0
SETOR = 1
#GRUPO = 2
LOJA = 3
#NOME_LOJA = 4
UF_LOJA = 5
#STATUS_ITEM = 6
ITEM = 7
DESCRICAO_PRODUTO = 8
VENDA_ULTIMOS_90_DIAS = 9
#DIAS_SEM_VENDA = 10
#PERDA_VENDAS_EM_UNIDADES = 11
#PERDA_VENDAS_EM_REAIS = 12
#DIAS_SEM_VENDA_ULTIMOS_90_DIAS = 13
#ESTOQUE_LOJA = 14
#PEDIDO_PENDENTE_LOJA = 15
#ESTOQUE_LOJA_E_PEDIDO_PENDENTE_LOJA = 16
#COBERTURA_ESTOQUE = 17
#SUJESTAO_HOJE = 18
#SUJESTAO_ESTOQUE_ZERO = 19
#QUANTIDADE_ULTIMA_ENTRADA_ESTOQUE = 20
#DATA_ULTIMA_ENTRADA_ESTOQUE_NA_LOJA = 21
#DATA_ULTIMA_POSICAO_ESTOQUE = 22
#ESTOQUE_CD_ABASTECEDOR = 23
#DATA_ULTIMA_ENTRADA_ESTOQUE_CD = 24
#QUANTIDADE_PEDIDO_PENDENTE_CD_ABASTECEDOR = 25
#CUSTO_ITEM = 26
#PRECO_SISTEMA = 27
#PRAZO_ENTREGA_CD = 28
#PRAZO_ENTREGA_FORNECEDOR = 29

INDEX = 'ruptura'
TYPE = 'ruptura'
FILE_NAME_PREFIX = 'ruptura'

from els.utils import ElasticFilesGenerator
from bd.materiales import Materiales
from bd.secciones import Secciones
from els.lang import Lang

materiales = Materiales.get_instance()
secciones = Secciones.get_instance()
L = Lang.get_instance()

class NoDataRecordException(Exception):
    pass

def parse(line):
    register = line.split('\t')
    if len(register) < 30:
        raise NoDataRecordException(u'Registro de datos no encontrado')
    for i in range(len(register)):
        register[i] = register[i].strip()
    return ({
        #"fornecedor": register[FORNECEDOR],
        #"setor": register[SETOR],
        L.loja: register[LOJA],
        #"uf_loja": register[UF_LOJA],
        L.material: register[ITEM],
        L.descricao_material: register[DESCRICAO_PRODUTO],
        "venda_ultimos_90_dias": float(register[VENDA_ULTIMOS_90_DIAS].strip('"').replace('.','').replace(',','.')), 
        })


def read(filename):

    lineNum = 0
    head, tail = ntpath.split(filename)
    data = datetime.datetime(
             int(tail[0:4]), int(tail[5:7]), int(tail[8:10]), 12
             ) - datetime.timedelta(days=1)
    efg = ElasticFilesGenerator(INDEX,TYPE,'%s.%s' % (FILE_NAME_PREFIX, str(data.date())))
    data = str(data)

    with open(filename, 'r') as f:
        for line in f:
            lineNum = lineNum + 1
            if lineNum <= 10:
                continue

            line = line.strip()
            line = line.decode("utf8","replace")
            try:
                register = parse(line)
                if register[L.loja][0] <> 'B':
                    register[L.loja] = 'B' + register[L.loja]
                register[L.data] = data
                register[L.ruptura] = 1
                register[L.perda] = - register['venda_ultimos_90_dias'] / 90 
                register[L.matid] = '%s%s' % (register[L.loja], register[L.material])
                register[L.secao] = materiales.get_seccion(register[L.material])
                register[L.descricao_secao] = secciones.get_descripcion(register[L.secao])
                register.pop('venda_ultimos_90_dias')

                efg.add(register, "%s%s" % (register[L.matid], str(register[L.data][0:10]).replace('-','')))

            except NoDataRecordException:
                pass
            #except Exception:
                #print(line)

for f in sys.argv[1:]:
    read(f)
