# !/usr/bin/env python
# -*- coding: UTF-8 -*-
from PyQt4 import QtGui
import sys

import yaml
from common.log.config import LogConfig
from common.log.manager import LogManager
from util.SingleInstance import SingleInstance, detection_dialog

__author__ = 'syc'

# 读取配置
config_file = open("./configs.yaml")
Load_configs = yaml.load(config_file)
app_file_name = Load_configs['app_file_name']
remote = Load_configs['remote']
host = remote['host']
port = remote['port']
url = remote['url']
access_type = remote['access_type']

LogConfig.LOG_TO_FILE = True
LogConfig.LOG_DIR = "Logs"
LogConfig.LOG_NAME = "upgrade_client"
LogManager.init()

kwargs = {
    'host': host,
    'port': port,
    'access_type': access_type
}

if __name__ == '__main__':

    from ui.MainWindow import MainWindow
    app = QtGui.QApplication(sys.argv)
    my_app = SingleInstance()
    if my_app.already_running():
        print "Another instance of this program is already running"
        detection_dialog()
        exit(0)

    w = MainWindow()
    w.show()
    sys.exit(app.exec_())


