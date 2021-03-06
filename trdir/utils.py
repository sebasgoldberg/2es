#!/usr/bin/python
#encoding=utf8


import json
import ntpath

class ElasticFilesGenerator:

    def __init__(self, iv_index, iv_type, iv_file_name_prefix, preserve_path=False):

        self.command_line = {
            "index": {
                "_index": iv_index,
                "_type": iv_type,
            }}

        self.command_line_delete = {
            "delete": {
                "_index": iv_index,
                "_type": iv_type,
            }}

 
        self.CANT_REGS_FILE=50000
        self.nreg=0
        self.fsalida=None

        if preserve_path:
            self.file_name_prefix = iv_file_name_prefix
        else:
            head, tail = ntpath.split(iv_file_name_prefix)
            self.file_name_prefix = tail

    def __del__(self):
        if self.fsalida is not None:
            self.fsalida.close()

    def do_file_control(self):

        if (self.nreg % self.CANT_REGS_FILE) == 0:
            nfile = int(self.nreg / self.CANT_REGS_FILE)
            if self.fsalida is not None:
                self.fsalida.close()
            self.fsalida = open("%s.%s.json" % (self.file_name_prefix, str(nfile)),"w")

        self.nreg = self.nreg + 1
   
    def add(self, iv_object, iv_id=None):

        self.do_file_control()

        if iv_id is not None:
            self.command_line['index'].update({ '_id': iv_id })

        json.dump(self.command_line, self.fsalida)
        self.fsalida.write('\n')
        json.dump(iv_object, self.fsalida)
        self.fsalida.write('\n')


    def index(self, iv_object, iv_id=None):
        self.add(iv_object, iv_id)

    def delete(self, iv_id):
        self.do_file_control()
        self.command_line_delete['delete'].update({ '_id': iv_id })
        json.dump(self.command_line_delete, self.fsalida)
        self.fsalida.write('\n')
