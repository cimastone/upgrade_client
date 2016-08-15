# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QVBoxLayout
from ui.Upgrade import Upgrade

__author__ = 'syc'


class MyEditText(QWidget):
    finishUpgrade = QtCore.pyqtSignal()
    startUpgrade = QtCore.pyqtSignal(dict)

    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.resize(600, 300)
        layout = QVBoxLayout()
        self.textEdit = QtGui.QTextEdit()
        self.textEdit.setReadOnly(True)
        layout.addWidget(self.textEdit)

        self.progress = QtGui.QProgressBar(self)
        self.progress.setGeometry(200, 80, 250, 20)
        layout.addWidget(self.progress)
        self.setLayout(layout)

        self.startUpgrade.connect(self.start_upgrade)  # 连接子进程的信号和槽函数
        self.upgrade = None
        self.completed = 0

    def start_upgrade(self, info):
        self.upgrade = Upgrade(info)
        self.upgrade.progressSignal.connect(self.set_content)  # 连接子进程的信号和槽函数
        self.upgrade.start()  # 开始执行 run() 函数里的内容

    def set_content(self, result):
        flag = result[0]
        content = result[1]
        if flag:
            self.completed += 20
            self.progress.setValue(self.completed)

        if content:
            self.textEdit.append(content)
        else:
            self.hide()
            self.completed = 0
            self.progress.setValue(self.completed)
            self.textEdit.clear()
            self.finishUpgrade.emit()

