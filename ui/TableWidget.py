# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TableWidget.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1403, 864)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.widget_cp = QtGui.QWidget(self.centralwidget)
        self.widget_cp.setGeometry(QtCore.QRect(0, 0, 961, 461))
        self.widget_cp.setObjectName(_fromUtf8("widget_cp"))
        self.tableWidget_client_list = QtGui.QTableWidget(self.widget_cp)
        self.tableWidget_client_list.setGeometry(QtCore.QRect(0, 40, 961, 401))
        self.tableWidget_client_list.setMaximumSize(QtCore.QSize(961, 16777215))
        self.tableWidget_client_list.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget_client_list.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget_client_list.setObjectName(_fromUtf8("tableWidget_client_list"))
        self.tableWidget_client_list.setColumnCount(7)
        self.tableWidget_client_list.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_client_list.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_client_list.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_client_list.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_client_list.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_client_list.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_client_list.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_client_list.setHorizontalHeaderItem(6, item)
        self.label_basket_list_2 = QtGui.QLabel(self.widget_cp)
        self.label_basket_list_2.setGeometry(QtCore.QRect(0, 20, 101, 16))
        self.label_basket_list_2.setObjectName(_fromUtf8("label_basket_list_2"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Robot测试客户端", None))
        item = self.tableWidget_client_list.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "appID", None))
        item = self.tableWidget_client_list.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "本地版本", None))
        item = self.tableWidget_client_list.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "服务器版本", None))
        item = self.tableWidget_client_list.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "服务端client", None))
        item = self.tableWidget_client_list.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "本地client", None))
        item = self.tableWidget_client_list.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "启动/升级", None))
        item = self.tableWidget_client_list.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "修复", None))
        self.label_basket_list_2.setText(_translate("MainWindow", "客户端应用列表：", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

