#!/usr/bin/env python3
# coding=utf-8

from build import Builder

build_dir="/home/gavin/github/drone"
#build_dir="/home/gavin/tmp/test_project"
b=Builder(build_dir)
b.create_docker_dir()
b.create_docker_file()
b.create_run_file()
b.build_docker_image()
b.build_sources()
