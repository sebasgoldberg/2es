#!/usr/bin/python
#encoding=utf8
__author__ = 'JSGold'

import datetime
import sys

BANDEIRA = 0
REGIONAL = 1
ESTABELECIMENTO = 2
MATRICULA = 3
NOME = 4
CARGO = 5
DIRETORIA = 6
UNIDAD_LOTACAO = 7
ADMISSAO = 8
PERFIL = 9
STATUS = 10
DESC_STATUS = 11
NASCIMENTO = 12
FAIXA_ETARIA = 13
SEXO = 14
TEMPO_CASA = 15
MES = 16
UF_TRAB = 17
LOCALIDADE = 18

sys.path.append('./')
from els.utils import ElasticFilesGenerator

class NoDataRecordException(Exception):
    pass

class AprendizException(Exception):
    pass

def get_date(date):
    return datetime.datetime(*tuple(map(int,[date[6:10],date[3:5],date[0:2],12])))

def parse(line):
    register = line.split('\t')
    if len(register) < 19:
        raise NoDataRecordException(u'Registro de datos no encontrado')
    #register = register[1:-1]
    for i in range(len(register)):
        register[i] = register[i].strip()
    if register[0] == "BAND.":
        raise NoDataRecordException(u"El registro de cabecera no es un registro de datos")
    return ({"bandeira": register[BANDEIRA],
        "regional": register[REGIONAL],
        "estabelecimento": register[ESTABELECIMENTO],
        "matricula": register[MATRICULA],
        "nome": register[NOME],
        "cargo": register[CARGO],
        "diretoria": register[DIRETORIA],
        "unidad_lotacao": register[UNIDAD_LOTACAO],
        "admissao": get_date(register[ADMISSAO]),
        "perfil": register[PERFIL],
        #"status": register[STATUS],
        #"desc_status": register[DESC_STATUS],
        "nascimento": get_date(register[NASCIMENTO]),
        "faixa_etaria": register[FAIXA_ETARIA],
        "sexo": register[SEXO],
        "tempo_casa": register[TEMPO_CASA],
        #"mes": register[MES],
        "uf_trab": register[UF_TRAB],
        "localidade": register[LOCALIDADE],
        })

def perfilGPTW(nomina):
    if 'TECNICO' in nomina['cargo']:
        return u'Técnico'
    if nomina['perfil'] in ['ADMINISTRATIVO']:
        return u'Administrativo'
    if nomina['perfil'] in ['LIDERES', 'ESPECIALISTAS', 'COORD/SUPERVISÃO']:
        return u'Média Liderança'
    if nomina['perfil'] in ['GERENCIA']:
        return u'Gerente'
    if nomina['perfil'] in ['DIRETOR']:
        return u'Presidente/ Diretoria'
    if 'APRENDIZ' in nomina['cargo']:
        raise AprendizException()
    raise Exception(u'Perfil no definido para registro de nómina: %s' % nomina)

TEMPO_CASA_VALUES = [
    (3, u'Entre 0 a 3 meses'),
    (1*12, u'Entre 3 meses e 1 ano'),
    (2*12, u'Entre 1 ano e 2 anos'),
    (5*12, u'Entre 2 anos e 5 anos'),
    (10*12, u'Entre 5 anos e 10 anos'),
    (15*12, u'Entre 10 anos e 15 anos'),
    (20*12, u'Entre 15 anos e 20 anos'),
]

def tempoCasaGPTW(nomina):
    tempoCasaMeses = int((datetime.datetime.today() - nomina['admissao']).days * 12 / 365)
    for (topeMeses,rango) in TEMPO_CASA_VALUES:
        if tempoCasaMeses <= topeMeses:
            return rango
    return  u'Mais de 20 anos'

FAIXA_ETARIA_VALUES = [
    (20, u'Menos de 20 anos'),
    (24, u'Entre 20 e 24 anos'),
    (30, u'Entre 25 e 30 anos'),
    (40, u'Entre 31 e 40 anos'),
    (56, u'Entre 41 e 56 anos'),
]

def faixaEtariaGPTW(nomina):
    faixaEtariaAnos = int((datetime.datetime.today() - nomina['nascimento']).days / 365)
    for (topeAnos,rango) in FAIXA_ETARIA_VALUES:
        if faixaEtariaAnos <= topeAnos:
            return rango
    return  u'Mais de 56 anos'


def getAvaliacaoGrupo(grupo, item):
    if item[grupo] is None:
        return (0, 0)
    return item[grupo], 1

def getAvaliacao(nomina, item):
    avaliacao = item['avaliacao']
    quan_avaliacoes = 1

    avaliacaoGrupo, quan_avaliacoes_grupo = getAvaliacaoGrupo(nomina['perfil'], item)
    avaliacao = avaliacaoGrupo + avaliacao
    quan_avaliacoes = quan_avaliacoes_grupo + quan_avaliacoes

    avaliacaoGrupo, quan_avaliacoes_grupo = getAvaliacaoGrupo(nomina['tempo_casa'], item)
    avaliacao = avaliacaoGrupo + avaliacao
    quan_avaliacoes = quan_avaliacoes_grupo + quan_avaliacoes

    avaliacaoGrupo, quan_avaliacoes_grupo = getAvaliacaoGrupo(nomina['faixa_etaria'], item)
    avaliacao = avaliacaoGrupo + avaliacao
    quan_avaliacoes = quan_avaliacoes_grupo + quan_avaliacoes

    avaliacaoGrupo, quan_avaliacoes_grupo = getAvaliacaoGrupo(nomina['sexo'], item)
    avaliacao = avaliacaoGrupo + avaliacao
    quan_avaliacoes = quan_avaliacoes_grupo + quan_avaliacoes

    return avaliacao / quan_avaliacoes

def addInfoGPTW(nomina, GPTW):
    nomina['GPTW'] = []
    for ano, anodict in GPTW.iteritems():
        for visao, visaodict in anodict.iteritems():
            for item in visaodict['items']:
                avaliacao = getAvaliacao(nomina, item)
                nomina['GPTW'].append({
                    'ano': ano,
                    'visao': visao,
                    'dimensao': item['dimensao'],
                    'num_item': item['num_item'],
                    'item': item['item'],
                    'avaliacao': avaliacao,
                })
    return nomina

def toGPTW(nomina, GPTW):
    nomina['perfil'] = perfilGPTW(nomina)
    nomina['tempo_casa'] = tempoCasaGPTW(nomina)
    nomina['faixa_etaria'] = faixaEtariaGPTW(nomina)
    return addInfoGPTW(nomina, GPTW)


def read(filename, GPTW):

    lineNum = 0
    efg = ElasticFilesGenerator("nomina","nomina","nomina")

    with open(filename, 'r') as f:
        for line in f:

            line = line.strip()
            #line = line.decode("utf8","replace")
            try:
                nomina = toGPTW(parse(line), GPTW)
                nomina['admissao'] = str(nomina['admissao'])
                nomina['nascimento'] = str(nomina['nascimento'])
                efg.add(nomina, nomina['matricula'])

            except NoDataRecordException:
                pass
            except AprendizException:
                pass
            #except Exception:
                #print(line)


def createGPTWFromFile(arquivo):
    DIMENSAO = 0
    NUM_ITEM = 1
    ITEM = 2
    AVALIACAO = 3
    GPTW = []
    with open(arquivo, 'r') as f:
        lineNum = 0
        colunas = None
        dimensao = None
        for line in f:
            item = {}
            lineNum = lineNum + 1
            if lineNum == 1:
                continue
            line = line.decode('utf8')
            line.strip()
            register = line.split('\t')
            for i in range(len(register)):
                register[i] = register[i].strip()
            if lineNum == 2:
                colunas = register
                continue
            if lineNum in [3, 4]:
                continue
            if register[DIMENSAO] <> '':
                dimensao = register[DIMENSAO]
            if register[NUM_ITEM] == '':
                continue
            item['dimensao'] = dimensao
            item['num_item'] = register[NUM_ITEM]
            item['item'] = register[ITEM]
            item['avaliacao'] = int(register[AVALIACAO])
            for i in range(4,len(colunas)):
                if colunas[i] == '':
                    continue
                try:
                    item[colunas[i]] = int(register[i])
                except ValueError:
                    item[colunas[i]] = None
            GPTW.append(item)
    return GPTW

def createGPTW():

    GPTW_FOLDER = 'nomina'

    GPTW = {
        '2014': {
            'Area': {
                'arquivo': '%s/GPTW-2014-area.xls' % GPTW_FOLDER,
            },
            'Companhia': {
                'arquivo': '%s/GPTW-2014-companhia.xls' % GPTW_FOLDER,
            },
        },
        '2015': {
            'Area': {
                'arquivo': '%s/GPTW-2015-area.xls' % GPTW_FOLDER,
            },
            'Companhia': {
                'arquivo': '%s/GPTW-2015-companhia.xls' % GPTW_FOLDER,
            },
        },
    }

    for ano, anodict in GPTW.iteritems():
        for visao, visaodict in anodict.iteritems():
            GPTW[ano][visao]['items'] = createGPTWFromFile(visaodict['arquivo'])
    return GPTW

GPTW = createGPTW()

for f in sys.argv[1:]:
    read(f, GPTW)
