#!/usr/bin/env python3
# coding=utf-8

BASE_CONTENT="""# This file is created by script
# AUTHOR: Gavin Lin

#!/bin/bash

"""

from os import path
from common import remove_file

class new_Runfile:
    def __init__(self, workdspace):
        self.runfile = path.join(workdspace, "drun.sh")
        remove_file(self.runfile)
        self.fopen = open(self.runfile, 'w')
        self.fopen.write(BASE_CONTENT)

    def write_Command(self, command):
        self.fopen.write("%s\n"%command)

    def write_Done(self):
        self.fopen.close()

    def get_Runfile(self):
        return self.runfile
