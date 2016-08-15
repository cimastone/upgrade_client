# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from TableWidget import Ui_MainWindow

__author__ = 'syc'


class TableWidget(QtGui.QMainWindow, Ui_MainWindow):

    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.setupUi(self)


