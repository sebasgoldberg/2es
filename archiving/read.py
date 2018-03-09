#!/usr/bin/python
#encoding=utf8
__author__ = 'JSGold'

import datetime
import sys

date = datetime.datetime.now()
NOW = date.strftime("%Y/%m/%d %H:%M:%S")
YEAR = date.year
MONTH = date.month

OWNER = 0
SEGMENT = 1
PARTITION = 2
TYPE = 3
TABLE_SPACE = 4
SIZE_MB = 7
            
sys.path.append('./')
from els.utils import ElasticFilesGenerator

class NoDataRecordException(Exception):
    pass

class FixedWidthLineToShortException(Exception):
    pass

class DBTableDoesNotExist(Exception):
    pass

FIELDS_LENGTHS = (4, 2, 12, 40, 10, 10)
LENGTH_TO_IGNORE_BETW_FIELDS = 1

def from_fixed_width(line, lengths, ignore_between=0):

    if len(lengths) == 0:
        return []

    total_length = sum(lengths) + (len(lengths)-1)*ignore_between

    if len(line) < total_length:
        raise FixedWidthLineToShortException(u'Line to short.')

    idx_from = 0
    idx_to = lengths[0]
    fields = []
    fields.append(line[idx_from:idx_to])

    for i in lengths[1:]:
        idx_from = idx_to + ignore_between
        idx_to = idx_from + i
        fields.append(line[idx_from:idx_to])

    return fields

def from_separated(line, separator='\t'):
    line.strip()
    reg = []
    for value in line.split(separator):
        reg.append(value.strip())
    return reg

def to_float(num):
    return float(num.replace('.','').replace(',','.'))

def parse(line):
    #register = line.split('\t')
    register = from_separated(line)
    return { 'segment' : {
        "owner": register[OWNER],
        "name": register[SEGMENT],
        "partition": register[PARTITION],
        "type": register[TYPE],
        "table_space": register[TABLE_SPACE],
        "size": int(to_float(register[SIZE_MB])*1024*1024),
        }}


def read(filename, dbtables):

    lineNum = 0
    efg = ElasticFilesGenerator("archiving","archiving","archiving")

    with open(filename, 'r') as f:
        for line in f:
            lineNum = lineNum + 1
            if lineNum == 1:
                continue

            line = line.strip()

            archiving = parse(line)
            archiving["@timestamp"] = NOW

            try:
                dbtable = dbtables.get_from_segment_reg(archiving['segment'])
                archiving['dbtable'] = {
                    'name': dbtable.name,
                    'type': dbtable.type,
                    'sap_tables': list(dbtable.sap_tables),
                    'archiving_objects': list(dbtable.archiving_objects),
                    }
            except DBTableDoesNotExist:
                pass

            efg.add(archiving,'%s-%s-%s-%s-%s-%s-%s' % (
                YEAR,
                MONTH,
                archiving['segment']['owner'],
                archiving['segment']['name'],
                archiving['segment']['partition'],
                archiving['segment']['type'],
                archiving['segment']['table_space'],
                ))


class DBTable:

    ARCHIVING_OBJECT = 0
    SAP_TABLE = 1
    DB_TABLE = 2
    TYPE = 3

    def __init__(self, name):
        self.name = name
        self.sap_tables = set()
        self.archiving_objects = set()

    def add_reg(self, reg):
        self.type = reg[DBTable.TYPE]
        self.sap_tables.add(reg[DBTable.SAP_TABLE])
        if reg[DBTable.ARCHIVING_OBJECT] <> '':
            self.archiving_objects.add(reg[DBTable.ARCHIVING_OBJECT])

    @staticmethod
    def get_dbtable_name_from_reg(reg):
        if reg[DBTable.DB_TABLE] == '':
            return reg[DBTable.SAP_TABLE]
        return reg[DBTable.DB_TABLE]

class DBTablesManager:

    def __init__(self, f):
        self.dbtables = {}
        for line in f:
            reg = from_separated(line)
            dbtable_name = DBTable.get_dbtable_name_from_reg(reg)
            dbtable = self.dbtables.get(dbtable_name,DBTable(dbtable_name))
            dbtable.add_reg(reg)
            self.dbtables[dbtable_name] = dbtable

    def get_from_segment_reg(self, reg):

        segment = reg['name']
        owner = reg['owner']

        try:
            return self.dbtables[segment]
        except KeyError:
            if owner <> 'SAPSR3':
                raise DBTableDoesNotExist

        dbtable = None
        if segment.find('~') >= 0:
            dbtable = segment.split('~')[0]
        elif segment.find('^') >= 0:
            dbtable = segment.split('^')[0]
        else:
            dbtable = segment[:-2]

        try:
            return self.dbtables[dbtable]
        except KeyError:
            raise DBTableDoesNotExist


tables = None
with open(sys.argv[1], 'r') as f:
    tables = DBTablesManager(f)

for f in sys.argv[2:]:
    read(f, tables)
