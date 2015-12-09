#!/usr/bin/env python3
# coding=utf-8


from os import path,mkdir,chdir
from common import *
from dockerfile import new_Dockerfile
from runfile import new_Runfile
from config import BASE_URL
from docker import Client

class Builder:

    def __init__(self, workdir, yaml_file=".drone.yml"):
        self.__base_build_docker_dir = "/home/gavin/tmp/build_docker"
        self.workspace = workdir
        self.yaml_file = path.join(workdir, yaml_file)
        self.ydata, self.is_err = load_yaml(self.yaml_file)
        self.cli = Client(base_url=BASE_URL)
        self.errmsg=''


    def create_docker_dir(self):
        if self.is_err:
            return

        folder_name = create_folder_name(self.ydata.get('project'))
        self.build_docker_dir = path.join(self.__base_build_docker_dir, folder_name)
        remove_folder(self.build_docker_dir)
        try:
            mkdir(self.build_docker_dir)
        except FileNotFoundError:
            print ("mkdir error\n")
            self.is_err = True
            self.errmsg = "mkdir %s error"%(self.build_docker_dir)

        self.image_name = folder_name


    def create_docker_file(self):
        if self.is_err:
            return

        docker_creat = new_Dockerfile(self.build_docker_dir)

        image_name = self.ydata.get("image")
        docker_creat.write_From(image_name)

        envs = self.ydata.get("env", None)
        if envs:
            for env in envs:
                docker_creat.write_Env(env)

        pre_scripts = self.ydata.get("scripts", None)
        if pre_scripts:
            for pre_script in pre_scripts:
                docker_creat.write_Run(pre_script)

        #docker_creat.write_Volume("/data")

        docker_creat.write_Done()


    def create_run_file(self):
        if self.is_err:
            return

        runfile_creat = new_Runfile(self.workspace) 

        try:
            build_scripts = self.ydata.get("build").get("scripts")
        except AttributeError:
            build_scripts = None

        if build_scripts:
            for build_script in build_scripts:
                runfile_creat.write_Command(build_script)

        runfile_creat.write_Done()

        self.runfile = runfile_creat.get_Runfile()

        #+x
        cmd = "chmod +x %s"%(self.runfile)
        run_Command(cmd)


    def build_docker_image(self):
        if self.is_err:
            return

        self.__remove_self_image()

        docker_build = self.cli.build(path=self.build_docker_dir, rm=True, forcerm=True, tag=self.image_name, stream=True)

        for line in docker_build:
            line=eval(line)
            print(line)
            if line.get('errorDetail', None):
                print("build docker image error, errmsg:", line.get('errorDetail'))
                self.is_err=True
                self.errmsg = line.get('errorDetail').get('message')
            

    def build_sources(self):
        if self.is_err:
            return

        cid = self.cli.create_container(self.image_name, command='/bin/bash ./drun.sh', volumes=['/tmp/drone'], working_dir='/tmp/drone', host_config=self.cli.create_host_config(binds={self.workspace:{'bind':'/tmp/drone', 'mode': 'rw',}}))
        print (cid.get('Id'))
        response = self.cli.start(container=cid.get('Id'))

        attachs = self.cli.attach(cid.get('Id'), stream=True)
        for attach in attachs:
            print(attach)

        #logs=self.cli.logs(container=cid.get('Id'), stdout=True, stderr=False)
        #print("Logs:", logs)

        self.__remove_self_image()

        self.errmsg=self.cli.logs(container=cid.get('Id'), stdout=False, stderr=True)
        if self.errmsg:
            self.is_err=True
            print("Build source error, error message:%s"%(self.errmsg))
            return

        print("Compile source code sucessfully!")


    def __remove_self_image(self):
        if is_Image_Exist(self.image_name):
            self.cli.remove_image(image=self.image_name,force=True)
