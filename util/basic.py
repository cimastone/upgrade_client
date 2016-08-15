#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import zipfile
import hashlib
import shutil
from distutils.version import LooseVersion

__author__ = 'syc'


def checkhct(progress_name):
    """
    判断该程序名的进程是否有开启
    :param progress_name: 进程名
    :return:
    """
    if not progress_name:
        return False

    for line in os.popen('tasklist').readlines():  # tasklist 也可换成linux下打印所有进程的命令 ps aux
        pattern = re.compile(progress_name, re.I)  # 判断用正则更准确，也可以使用find或者index判断
        match = pattern.match(line)
        if match:
            return True
    return False


def get_app_path(root_dir):
    """
    得到后缀为.exe文件的路径
    """
    list_dirs = os.walk(root_dir)
    paths = []
    for root, dirs, files in list_dirs:
        paths = paths + [os.path.join(root, f) for f in files if '.exe' in f]

    return paths


def get_dirs(app_id):
    app_dir = os.getcwd()
    root_dir = os.path.join(app_dir, 'client', app_id)
    zip_dir = os.path.join(root_dir, 'zip')
    release_dir = os.path.join(root_dir, 'release')
    temp_dir = os.path.join(root_dir, 'temp')

    return root_dir, zip_dir, release_dir, temp_dir


def write_zip(**kwargs):
    """
    将服务端返回的内容写入zip文件中
    """
    root_dir, zip_dir, release_dir, temp_dir = get_dirs(kwargs['info']['app_id'])
    if not os.path.exists(zip_dir):
        os.makedirs(zip_dir)
    file_name = ''.join([kwargs['info']['app_id'], '_',  kwargs['info']['version'], '.zip'])
    f = open(os.path.join(zip_dir, file_name), 'wb')
    f.write(kwargs['response_data'])
    f.close()
    kwargs['thread'].progressSignal.emit([True, 'the lastest version already download'])
    return root_dir, zip_dir, file_name


def un_zip(file_name, root_dir):
    """
    unzip zip file
        file_name: 压缩包路径
    """
    zip_file = zipfile.ZipFile(file_name)
    temp_dir = os.path.join(root_dir, 'temp')

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    for names in zip_file.namelist():
        zip_file.extract(names, temp_dir)
    zip_file.close()
    return temp_dir


def remv_copy(release_dir, temp_dir):
    """
    删除源目录，将临时目录的内容写入源目录，将临时目录删除
    :param release_dir:
    :param temp_dir:
    :return:
    """
    shutil.rmtree(release_dir)
    shutil.copytree(temp_dir, release_dir, ignore=shutil.ignore_patterns('*.bak', 'logs*'))
    shutil.rmtree(temp_dir)


def md5_for_file(filepath, block_size=2**20):
    """
    以文件路径作为参数，返回对文件md5后的值
    """
    f = open(filepath, 'rb')
    md5 = hashlib.md5()
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()


def cmp_version(src, dest):
    """
    版本比较
    :param src: 第一个版本号
    :param dest: 第二版本号
    :return: src > dest: 大于0；src == dest :等于0； src < dest：小于0
    """
    if cmp(LooseVersion(src), LooseVersion(dest)) == 0:
        return True
    else:
        return False
