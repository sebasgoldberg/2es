#!/usr/bin/python
#encoding=utf8

import datetime
import sys

#sys.path.append('./')
from utils import ElasticFilesGenerator

efg = ElasticFilesGenerator("trdir","trdir",'../bulk/trdir', preserve_path=True)

class NoDataRecordException(Exception):
    pass

class FixedWidthLineToShortException(Exception):
    pass

def read(filename):

    lineNum = 0

    with open(filename, 'r') as f:
        trdir = {
            'name': filename,
            'src': f.read(),
            }
        efg.add(trdir)

for f in sys.argv[1:]:
    read(f)
