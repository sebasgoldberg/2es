#!/usr/bin/python
#encoding=utf8
__author__ = 'JSGold'

import datetime
import sys

sys.path.append('./')
from els.utils import ElasticFilesGenerator

NOTA = 0
SERIE = 1
CNPJ = 2
PEDIDO = 3
FORNECEDOR = 4
DATA_EMISSAO = 5
DATA_CRIACAO = 6
TOTAL_PRODUTO = 7
TOTAL_NOTA = 8
ENVIADA_SAP = 9
CENTRO = 10
TIPO_CENTRO = 11
ORG_VENDA = 12
ERRO_REMESSA = 13
ERRO_CADASTRO = 14
ERRO_COMERCIAL = 15
ERRO_CUSTO_REAL = 16
ERRO_EMBALAGEM = 17
ERRO_FISCAL = 18
ERRO_MATERIAL = 19
ERRO_QUANTIDADE = 20
ERRO_OPERACIONAL = 21
ERRO_CUSTO = 22
NOME_FANTASIA = 23
DIA = 24
MES = 25
SEMANA = 26
CHECK_NFS = 27
CHECK_PEDIDO = 28
CONSOLIDADO_SUPPLY = 29
HORTI = 30


class NoDataRecordException(Exception):
    pass

def get_data(datahora):
    """
    data: 02/01/2016  00:00:00
    """
    data, hora = datahora.split(' ')
    data = list(map(int,data.split('/')))
    hora = list(map(int,hora.split(':')))
    return datetime.datetime(data[2], data[1], data[0], hora[0], hora[1])

def get_float(value):
    return float(value.replace('.','').replace(',','.'))

def parse(line):
    register = line.split('\t')
    if len(register) < 31:
        raise NoDataRecordException(u'Registro de datos no encontrado')
    for i in range(len(register)):
        register[i] = register[i].strip()
    return ({
        'nota': register[NOTA],
        'serie': register[SERIE],
        'cnpj': register[CNPJ],
        'pedido': register[PEDIDO],
        'fornecedor': register[FORNECEDOR],
        'data_emissao': get_data(register[DATA_EMISSAO]),
        'data_criacao': get_data(register[DATA_CRIACAO]),
        'total_produto': get_float(register[TOTAL_PRODUTO]),
        'total_nota': get_float(register[TOTAL_NOTA]),
        'enviada_sap': register[ENVIADA_SAP],
        'centro': register[CENTRO],
        'tipo_centro': register[TIPO_CENTRO],
        'org_venda': register[ORG_VENDA],
        'erro_remessa': int(register[ERRO_REMESSA]),
        'erro_cadastro': int(register[ERRO_CADASTRO]),
        'erro_comercial': int(register[ERRO_COMERCIAL]),
        'erro_custo_real': int(register[ERRO_CUSTO_REAL]),
        'erro_embalagem': int(register[ERRO_EMBALAGEM]),
        'erro_fiscal': int(register[ERRO_FISCAL]),
        'erro_material': int(register[ERRO_MATERIAL]),
        'erro_quantidade': int(register[ERRO_QUANTIDADE]),
        'erro_operacional': int(register[ERRO_OPERACIONAL]),
        'erro_custo': int(register[ERRO_CUSTO]),
        'nome_fantasia': register[NOME_FANTASIA],
        'dia': int(register[DIA]),
        'mes': int(register[MES]),
        'semana': register[SEMANA],
        'check_nfs': register[CHECK_NFS],
        'check_pedido': register[CHECK_PEDIDO],
        'consolidado_supply': int(register[CONSOLIDADO_SUPPLY]),
        'horti': register[HORTI],
        })


def add_tipo_erro(nfe):

    nfe['tipo_erro'] = []

    if nfe['erro_remessa'] == 1:
        nfe['tipo_erro'].append('remessa')
    if nfe['erro_cadastro'] == 1:
        nfe['tipo_erro'].append('cadastro')
    if nfe['erro_comercial'] == 1:
        nfe['tipo_erro'].append('comercial')
    if nfe['erro_custo_real'] == 1:
        nfe['tipo_erro'].append('custo_real')
    if nfe['erro_embalagem'] == 1:
        nfe['tipo_erro'].append('embalagem')
    if nfe['erro_fiscal'] == 1:
        nfe['tipo_erro'].append('fiscal')
    if nfe['erro_material'] == 1:
        nfe['tipo_erro'].append('material')
    if nfe['erro_quantidade'] == 1:
        nfe['tipo_erro'].append('quantidade')
    if nfe['erro_operacional'] == 1:
        nfe['tipo_erro'].append('operacional')
    if nfe['erro_custo'] == 1:
        nfe['tipo_erro'].append('custo')


def set_quan_erros(nfe):
    if nfe['check_nfs'] == 'C/ Erro':
        nfe['quan_erros'] = 1
    else:
        nfe['quan_erros'] = 0


def read(filename):

    lineNum = 0
    efg = ElasticFilesGenerator("nfe","nfe","nfe")

    with open(filename, 'r') as f:
        for line in f:
            lineNum = lineNum + 1
            if lineNum < 2:
                continue

            line = line.strip()
            try:
                nfe = parse(line)
                nfe['data_emissao'] = str(nfe['data_emissao'])
                nfe['data_criacao'] = str(nfe['data_criacao'])
                add_tipo_erro(nfe)
                set_quan_erros(nfe)
                efg.add(nfe,'%(cnpj)s-%(serie)s-%(nota)s' % nfe)

            except NoDataRecordException:
                pass
            #except Exception:
                #print(line)

for f in sys.argv:
    read(f)
