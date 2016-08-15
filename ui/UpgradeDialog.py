# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

__author__ = 'syc'


class Dialog(QtGui.QDialog):
    startDialog = QtCore.pyqtSignal(dict)
    finishDialog = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.resize(240, 200)
        grid = QtGui.QGridLayout()  # 表格布局，用来布局QLabel和QLineEdit及QSpinBox
        grid.addWidget(QtGui.QLabel(u'应用名称：', parent=self), 0, 0, 1, 1)
        self.app_name = QtGui.QLabel('', parent=self)
        grid.addWidget(self.app_name, 0, 1, 1, 1)

        grid.addWidget(QtGui.QLabel(u'版本号：', parent=self), 1, 0, 1, 1)
        self.version = QtGui.QLabel('', parent=self)
        grid.addWidget(self.version, 1, 1, 1, 1)

        grid.addWidget(QtGui.QLabel(u'版本描述：', parent=self), 2, 0, 1, 1)
        self.ver_desc = QtGui.QLabel('', parent=self)
        grid.addWidget(self.ver_desc, 2, 1, 1, 1)

        buttonBox = QtGui.QDialogButtonBox(parent=self)  # 创建ButtonBox，用户确定和取消
        buttonBox.setOrientation(QtCore.Qt.Horizontal)  # 设置为水平方向
        buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)  # 确定和取消两个按钮
        self.startDialog.connect(self.set_label_text)  # 连接子进程的信号和槽函数
        buttonBox.accepted.connect(self.accept)  # 确定
        buttonBox.rejected.connect(self.reject)  # 取消

        layout = QtGui.QVBoxLayout()  # 垂直布局，布局表格及按钮
        layout.addLayout(grid)  # 加入前面创建的表格布局
        spacerItem = QtGui.QSpacerItem(20, 48, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)  # 间隔对象美化布局
        layout.addItem(spacerItem)
        layout.addWidget(buttonBox)  # ButtonBox

        self.setLayout(layout)
        self.sever_client = None

    def accept(self):
        self.hide()
        self.finishDialog.emit(self.sever_client)

    def set_label_text(self, server_client):
        self.sever_client = server_client
        self.app_name.setText(server_client.get('app_id'))
        self.version.setText(server_client.get('version'))
        self.ver_desc.setText('this version have not describe'
                              if not server_client.get('ver_desc') else server_client.get('ver_desc'))
        self.ver_desc.setWordWrap(True)


