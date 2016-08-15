# -*- coding: utf-8 -*-
import yaml

__author__ = 'syc'


def empty_file(file_path):
    """
    判断该文件是否是空文件
    :param filepath: 文件路径
    :return: （bool）空文件：True,非空文件：False
    """
    stream = file(file_path, 'r')
    lines = stream.readlines()
    flag = True
    non_empty_line = filter(lambda line: line is False, lines)
    if non_empty_line:
        flag = False

    return flag


def load_file(file_path):
    """
    load所有client的信息
    :param file_path: 文件路径
    :return:
    """
    stream = file(file_path, 'a+')
    local_info = yaml.load(stream)
    if not local_info:
        local_info = dict()
    return local_info


def cover_file(data, file_path):
    """
    覆盖文件数据
    :param file_path: 文件路径
    :return:
    """
    stream = file(file_path, 'w')
    yaml.dump(data, stream, default_flow_style=False, explicit_start=True, explicit_end=True)


def apped_file(data, file_path):
    """
    追加文件数据
    :param filepath: 文件路径
    :return:
    """
    stream = file(file_path, 'a')
    for enum in data.items():
        yaml.dump(enum, stream, default_flow_style=False, explicit_start=True, explicit_end=True)
