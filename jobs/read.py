#!/usr/bin/env python3
#encoding=utf8
__author__ = 'JSGold'

import datetime
import sys

OWNER = 0
SEGMENT = 1
PARTITION = 2
TYPE = 3
TABLE_SPACE = 4
SIZE_MB = 7
            
sys.path.append('./')
from els.utils import ElasticFilesGenerator
efg = ElasticFilesGenerator("jobs","jobs","jobs")

def from_separated(line, separator='\t'):
    line.strip()
    reg = []
    for value in line.split(separator):
        reg.append(value.strip())
    return reg

def to_float(num):
    return float(num.replace('.','').replace(',','.'))

def apply_tz(date):
    return date - datetime.timedelta(seconds=-3*60*60)

def to_datetime(date='99991231', time='000000'):
    
    return apply_tz(datetime.datetime.strptime('%s %s' % (date, time), '%d.%m.%Y %H:%M:%S'))

def format_datetime(dt):
    return dt.strftime("%Y/%m/%d %H:%M:%S")

def to_es_datetime(date, time):
    return format_datetime(to_datetime(date, time))

def to_es_timestamp_range(dtfrom, dtto, td=5*60):
    dt = dtfrom
    td = datetime.timedelta(seconds=td)
    while dt <= dtto:
        yield format_datetime(dt)
        dt = dt + td

def to_es_timedelta_minutes(dtfrom, dtto, td=60):
    return float((dtto - dtfrom).total_seconds()) / 60

class NoDataException(Exception):
    pass

class JobNaoIniciadoException(Exception):
    pass

def parse(line):

    JOBNAME = 1-1
    JOBCOUNT = 2-1
    LASTCHDATE = 12-1
    LASTCHTIME = 13-1
    LASTCHNAME = 14-1
    STRTDATE = 18-1
    STRTTIME = 19-1
    ENDDATE = 20-1
    ENDTIME = 21-1
    STATUS = 30-1
    BTCSYSREAX = 43-1
    REAXSERVER = 53-1

    register = from_separated(line)
    #print(line)
    #print(register)

    if len(register) < (JOBCOUNT+1):
        raise NoDataException()

    if register[JOBCOUNT] == '' or register[JOBCOUNT] == 'Nº job':
        raise NoDataException()

    if register[STRTDATE] == '':
        raise JobNaoIniciadoException()

    start_date = to_datetime(register[STRTDATE],register[STRTTIME])

    if register[ENDDATE] == '':
        end_date = apply_tz(datetime.datetime.now())
    else:
        end_date = to_datetime(register[ENDDATE],register[ENDTIME])

    for t in to_es_timestamp_range(
        start_date,
        end_date
        ):

        yield { 
            "ID": '%s-%s' % (register[JOBNAME], register[JOBCOUNT]),
            "jobname": register[JOBNAME],
            "jobnumber": register[JOBCOUNT],
            "autor_modif": register[LASTCHNAME],
            "@timestamp_execucao": t,
            "@timestamp_modif": to_es_datetime(register[LASTCHDATE],register[LASTCHTIME]),
            "duracao_em_minutos": to_es_timedelta_minutes(
                    start_date,
                    end_date),
            "sistema": register[BTCSYSREAX],
            "servidor": register[REAXSERVER],
            "status": register[STATUS],
            }


def read(filename):

    lineNum = 0
    
    with open(filename, 'r') as f:
        for line in f:
            lineNum = lineNum + 1
            if lineNum == 1:
                continue

            line = line.strip()

            try:
                for jobs in parse(line):

                    efg.add(jobs,'%s-%s-%s' % (
                        jobs['jobname'],
                        jobs['jobnumber'],
                        jobs['@timestamp_execucao'],
                        ))

            except JobNaoIniciadoException:
                pass
            except NoDataException:
                pass
            #except:
            #    print('ERRO em linea: %s' % line)


import argparse

parser = argparse.ArgumentParser(description='Gera arquivos json para ser carregados no elasticsearch.')
parser.add_argument('files', nargs='+', metavar='f',
                    help='Arquivo com o formato  de texto separado por tabuladores com todas as columnas da tabela TBTCO (jobs SAP).')

args = parser.parse_args()

for f in args.files:
    read(f)
