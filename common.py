#!/usr/bin/env python3
# coding=utf-8

import yaml
from datetime import date
from random import randint
from shutil import rmtree
from os import path, remove, system
from config import BASE_URL
from docker import Client, errors

def load_yaml(yaml_file):
    ydata = None
    is_err = True
    try:
        fdata = open(yaml_file, 'r')
    except FileNotFoundError:
        return ydata, is_err

    ydata = yaml.load(fdata)

    if type(ydata) == dict:
        is_err = False

    return ydata,is_err

def create_folder_name(name):
    today = date.today().strftime("%d%m%y")
    rand_int = str(randint(1000,9999))
    name_list = [today,rand_int,name]
    return '_'.join(name_list)

def remove_folder(folder):
    if path.exists(folder):
        rmtree(folder)

def remove_file(filename):
    if path.exists(filename):
        remove(filename)

def run_Command(cmd):
    is_err = system(cmd)
    return is_err

def is_Image_Exist(imagename):
    cli = Client(base_url=BASE_URL)
    try:
        image_history = cli.history(imagename)
    except errors.NotFound:
        image_history = None

    return image_history

