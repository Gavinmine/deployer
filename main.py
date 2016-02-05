#!/bin/python3
#coding=utf-8

from build import Builder

build_dir="/home/wlsuser/gavin/branches/integration_CM/WBEService"
b=Builder(build_dir)
b.create_docker_dir()
b.create_docker_file()
b.create_run_file()
b.build_docker_image()
b.build_sources()
