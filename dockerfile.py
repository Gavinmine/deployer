#!/usr/bin/env python3
# coding=utf-8

BASE_CONTENT="""# This dockerfile uses the ubuntu image
# Version 2 - EDITION 1
# Author: Gavin Lin


"""

from os import path

class new_Dockerfile:
    def __init__(self, build_dir):
        self.dockerfile = path.join(build_dir, "Dockerfile")
        self.fopen = open(self.dockerfile, 'w')
        self.fopen.write(BASE_CONTENT)

    def write_From(self, image):
        self.fopen.write("FROM %s\n"%image)

    def write_Maintainer(self, maintainer):
        self.fopen.write("MAINTAINER from %s\n"%maintainer)

    def write_Run(self, command):
        self.fopen.write("RUN %s\n"%command)

    def write_CMD(self, command):
        self.fopen.write("CMD %s\n"%command)

    def write_Expose(self, expose):
        self.fopen.write("EXPOSE %s\n"%expose)

    def write_Env(self, env):
        self.fopen.write("ENV %s\n"%env)

    def write_Add(self, src, dest):
        self.fopen.write("Add %s %s\n"%(src, dest))

    def write_Copy(self, src, dest):
        self.fopen.write("COPY %s %s\n"%(src, dest))

    def write_Entrypoint(self, entrypoint):
        self.fopen.write("ENTRYPOINT %s\n"%entrypoint)

    def write_Volume(self, volume):
        self.fopen.write('VOLUME ["%s"]\n'%volume)

    def write_User(self, user):
        self.fopen.write("USER %s\n"%user)

    def write_Workdir(self, workdir):
        self.fopen.write("WORKDIR %s\n"%workdir)

    def write_Onbuild(self, onbuild):
        self.fopen.write("ONBUILD %s\n"%onbuild)

    def write_Done(self):
        self.fopen.close()
