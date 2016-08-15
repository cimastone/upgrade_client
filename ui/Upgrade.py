# -*- coding: utf-8 -*-
from os import listdir
import os
from PyQt4 import QtCore
from main import kwargs
from main import app_file_name
from upgrade_detection import http_request
from upgrade_detection import local_operation
from util.basic import get_dirs
from util.yamls import load_file
from util.yamls import cover_file

__author__ = 'syc'


class Upgrade(QtCore.QThread):
    """版本升级线程"""
    progressSignal = QtCore.pyqtSignal(list)

    def __init__(self, info, parent=None):
        super(Upgrade, self).__init__(parent)
        self.info = info

    def run(self):
        app_dir = os.getcwd()
        kwargs['url'] = '/upgrade/zip'
        kwargs['app_dir'] = app_dir
        kwargs['request_dict'] = dict(filepath=self.info['app_path'])
        kwargs['info'] = self.info
        kwargs['thread'] = self

        root_dir, zip_dir, release_dir, temp_dir = get_dirs(self.info['app_id'])
        if os.path.exists(zip_dir):
            file_name = ''.join([self.info['app_id'], '_',  self.info['version'], '.zip'])
            files = [f for f in listdir(zip_dir) if f == file_name]
            if files:
                self.progressSignal.emit([True, 'download package detection success'])
                client_app_path = local_operation(root_dir, zip_dir, file_name, **kwargs)
            else:
                self.progressSignal.emit([False, '%s have lasest version:%s,perpare upgrade...' %
                                          (self.info['app_id'], self.info['version'])])
                client_app_path = http_request(**kwargs)
        else:
            self.progressSignal.emit([False, '%s have lasest version:%s,perpare upgrade...' %
                                      (self.info['app_id'], self.info['version'])])
            client_app_path = http_request(**kwargs)

        self.info['app_path'] = client_app_path
        file_path = os.path.join(app_dir, app_file_name)
        local_info = load_file(file_path)

        local_info[self.info['app_id']] = self.info
        cover_file(local_info, app_file_name)
        self.progressSignal.emit([False, ''])
