# -*- coding: UTF-8 -*-
from PyQt4 import QtGui

from win32api import GetLastError
from win32api import CloseHandle
from win32event import CreateMutex
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QDialog
from winerror import ERROR_ALREADY_EXISTS

__author__ = 'syc'


class SingleInstance(object):
    """ Limits application to single instance """

    def __init__(self):
        self.mutexname = "testmutex_{D0E858DF-985E-4907-B7FB-8D732C3FC3B9}"
        self.mutex = CreateMutex(None, False, self.mutexname)
        self.lasterror = GetLastError()

    def already_running(self):
        return self.lasterror == ERROR_ALREADY_EXISTS

    def __del__(self):
        if self.mutex:
            CloseHandle(self.mutex)


def detection_dialog():
    """
    启动检测对话框
    """
    dialog = QDialog()
    dialog.resize(200, 100)
    prompt = QtGui.QLabel(u'已经有一个实例在运行', dialog)
    prompt.setGeometry(50, 40, 200, 20)
    dialog.setWindowTitle(u"提示")
    dialog.setWindowModality(Qt.ApplicationModal)

    dialog.exec_()
