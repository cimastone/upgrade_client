# -*- coding: utf-8 -*-
import os
import json
import httplib
from common.log.manager import LogManager
from util.basic import md5_for_file
from util.basic import write_zip
from util.basic import remv_copy
from util.basic import get_app_path
from util.basic import un_zip

__author__ = 'syc'

logger = LogManager.register_log("upgrade_detection")


def http_request(**kwargs):
    """
    连接服务端，解析服务端返回的数据
    """
    resp_dict = {
        'text/html; charset=utf-8': resp_json,
        'application/zip': resp_zip,
    }
    conn = httplib.HTTPConnection(kwargs['host'], kwargs['port'])
    body = json.dumps(kwargs['request_dict'])
    try:
        conn.request(kwargs['access_type'], kwargs['url'], body, headers={"Content-Type": "application/json"})
    except Exception as e:
        msg = 'connect upgrade service server failed: %s' % e
        emit_signal(msg, **kwargs)

    response = conn.getresponse()
    if response.status != 200:
        msg = 'upgrade service server response exception'
        emit_signal(msg, **kwargs)

    response_data = response.read()
    kwargs['response_data'] = response_data

    return resp_dict[response.getheader('Content-Type')](**kwargs)


def resp_json(**kwargs):
    """
    处理升级服务返回的json数据
    :param response:
    :return:
    """
    response_body = json.loads(kwargs['response_data'])
    if response_body['code'] != 0:
        msg = response_body['data']
        emit_signal(msg, **kwargs)

    return response_body


def resp_zip(**kwargs):
    """
    处理升级服务返回的zip数据
    :param response: exe文件路径
    :return:
    """
    root_dir, zip_dir, file_name = write_zip(**kwargs)  # 将服务端返回内容写入zip文件
    if kwargs['info']['md5'] != md5_for_file(os.path.join(zip_dir, file_name)):  # 判断MD5
        msg = '%s app download is not fully' % kwargs['info']['app_id']
        emit_signal(msg, **kwargs)
    else:
        kwargs['thread'].progressSignal.emit([True, 'download package detection success'])

    return local_operation(root_dir, zip_dir, file_name, **kwargs)


def local_operation(root_dir, zip_dir, file_name, **kwargs):
    """
    zip下载本地后，进行一系列的本地操作
    :param root_dir: 根目录
    :param zip_dir: zip文件存放目录
    :param file_name: zip文件名称
    :param kwargs:
    :return:
    """

    temp_dir = un_zip(os.path.join(zip_dir, file_name), root_dir)  # 解压zip文件
    kwargs['thread'].progressSignal.emit([True, '%s app discompression is ok' % kwargs['info']['app_id']])

    release_dir = os.path.join(root_dir, 'release')  # 得到本地的发布目录
    if not os.path.exists(release_dir):
        os.makedirs(release_dir)

    kwargs['thread'].progressSignal.emit([True, 'start remove origin dectory and copy files'])
    remv_copy(release_dir, temp_dir)
    kwargs['thread'].progressSignal.emit([True, 'upgrade lastest version is ok'])

    paths = get_app_path(release_dir)
    if len(paths) != 1:
        msg = 'zip package have not suffix exe file or more than 1 suffix exe file'
        emit_signal(msg, **kwargs)

    return paths[0]


def emit_signal(msg, **kwargs):
    kwargs['thread'].progressSignal.emit([False, msg])
    raise Exception(msg)
