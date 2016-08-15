# -*- coding: utf-8 -*-
import os
from PyQt4 import QtCore
from main import app_file_name
from main import kwargs
from main import url
from upgrade_detection import http_request
from util.yamls import load_file

__author__ = 'syc'


class Detection(QtCore.QThread):
    """版本检测线程"""
    progressSignal = QtCore.pyqtSignal(list)
    detectionSignal = QtCore.pyqtSignal(list)

    def __init__(self, parent=None):
        super(Detection, self).__init__(parent)
        self.progressSignal.connect(self.detection_info)  # 检测服务和本地中的客户端版本
        self.local_info = {}
        self.server_info = {}

    def run(self):
        app_dir = os.getcwd()
        self.local_info = self.get_local_info(app_dir)
        kwargs['url'] = url
        kwargs['app_dir'] = app_dir
        kwargs['request_dict'] = {}
        kwargs['thread'] = self

        result = http_request(**kwargs)
        self.server_info = result['data']
        self.detectionSignal.emit([self.server_info, self.local_info, True])

    def detection_info(self, result):
        if result[0] is False:
            self.server_info = {}
            self.detectionSignal.emit([self.server_info, self.local_info, False])

    def get_local_info(self, app_dir):
        file_path = os.path.join(app_dir, app_file_name)
        local_info = load_file(file_path)
        return local_info
