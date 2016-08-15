# -*- coding: utf-8 -*-
import os
import json

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QPalette
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QTableWidgetItem
from PyQt4.QtGui import QMessageBox

from ui.Detection import Detection
from ui.MyEditText import MyEditText
from ui.MyTableWidget import TableWidget
from ui.UpgradeDialog import Dialog
from util.basic import get_dirs
from util.basic import remv_copy
from util.basic import un_zip
from util.basic import checkhct
from util.basic import cmp_version

__author__ = 'syc'


class MainWindow(QtGui.QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.resize(800, 500)
        self.table = TableWidget()
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.setWindowTitle('upgrade_client')

        self.edit_text = MyEditText()
        self.edit_text.hide()
        self.edit_text.finishUpgrade.connect(self.finish_upgrade)

        self.dialog = Dialog()
        self.dialog.hide()
        self.dialog.finishDialog.connect(self.finish_dialog)

        self.detection = Detection()  # 检测版本线程
        self.detection.detectionSignal.connect(self.get_detection_info)  # 检测服务和本地中的客户端版本
        self.detection.start()  # 执行run方法

        self.timer = QtCore.QTimer()
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.detection.start)
        self.timer.start(60000)

        self.button = None
        self.show_label = QtGui.QLabel(u'连接升级服务失败！', self)
        self.show_label.setWordWrap(True)
        self.show_label.setGeometry(10, -30, 200, 100)

    def finish_dialog(self, server_client):
        """
        更新对话框点击确认后
        """
        self.edit_text.show()
        self.edit_text.startUpgrade.emit(server_client)

    def get_detection_info(self, result):
        """
        系统每分钟向服务端进行版本检测，返回两种情况：1：（list）[False, msg]连接服务端出现错误
                                                      2：（list）[server_info, client_info]返回服务和本地中客户端信息
        """
        pe = QPalette()
        if result[2]:
            pe.setColor(QPalette.WindowText, Qt.darkGreen)  # 设置字体颜色
            self.show_label.setText(u'连接升级服务成功！')
        else:
            pe.setColor(QPalette.WindowText, Qt.red)  # 设置字体颜色
            self.show_label.setText(u'连接升级服务失败！')

        self.show_label.setPalette(pe)
        self.update_client_list(result)

    def update_client_list(self, result):
        """
        列出本地客户端的信息和服务中的客户端的版本号
        """
        server_info = result[0]  # 服务客户端信息
        local_info = result[1]  # 本地客户端信息
        union_key = set(server_info) | set(local_info)
        self.table.tableWidget_client_list.setRowCount(len(union_key))

        index = 0
        for app_id in union_key:
            local_ver = local_info.get(app_id, {'version': '0'})['version']
            server_ver = server_info.get(app_id, {'version': '0'})['version']
            self.table.tableWidget_client_list.setItem(index, 0, QTableWidgetItem(app_id))
            self.table.tableWidget_client_list.setItem(index, 1, QTableWidgetItem(local_ver))
            self.table.tableWidget_client_list.setItem(index, 2, QTableWidgetItem(server_ver))
            self.table.tableWidget_client_list.setItem(index, 3, QTableWidgetItem(json.dumps(server_info.get(app_id))))
            self.table.tableWidget_client_list.setItem(index, 4, QTableWidgetItem(json.dumps(local_info.get(app_id))))

            repair_button = QtGui.QPushButton(u'修复')
            if not server_ver and not local_ver:
                self.button.setEnabled(False)
                repair_button.setEnabled(False)
            elif server_ver is '0' or cmp_version(server_ver, local_ver):
                self.button = QtGui.QPushButton(u'启动')
                repair_button.clicked.connect(lambda: self.handle_button_clicked(butt_type=1))
            else:
                self.button = QtGui.QPushButton(u'更新')
                repair_button.setEnabled(False)

            self.button.clicked.connect(lambda: self.handle_button_clicked(2))
            self.table.tableWidget_client_list.setCellWidget(index, 5, self.button)
            self.table.tableWidget_client_list.setCellWidget(index, 6, repair_button)

            self.table.tableWidget_client_list.hideColumn(3)
            self.table.tableWidget_client_list.hideColumn(4)
            index += 1

    def handle_button_clicked(self, butt_type=1):
        button = QtGui.qApp.focusWidget()
        index = self.table.tableWidget_client_list.indexAt(button.pos())

        if index.isValid():
            server_client = json.loads(str(self.table.tableWidget_client_list.item(index.row(), 3).text()))
            local_client = json.loads(str(self.table.tableWidget_client_list.item(index.row(), 4).text()))

            if butt_type == 1:
                self.repair_clicked(local_client)
            elif butt_type == 2:
                self.upgrade_click(server_client, local_client, button)

    def repair_clicked(self, local_client):
        """
        本地客户端修复按钮click槽函数
        """
        app_exec = os.path.basename(local_client['app_path'])

        if checkhct(app_exec):
            if self.prompt(app_exec):
                self.reapir_client(local_client)
        else:
            self.reapir_client(local_client)

    def reapir_client(self, local_client):
        """
        将本地客户端进行修复或者是版本回退
        :param local_client: 本地的该app信息
        :return:
        """
        root_dir, zip_dir, release_dir, temp_dir = get_dirs(local_client['app_id'])
        file_name = ''.join([local_client['app_id'], '_', local_client['version'], '.zip'])
        temp_dir = un_zip(os.path.join(zip_dir, file_name), root_dir)

        remv_copy(release_dir, temp_dir)
        self.repair_dialog(local_client)

    def upgrade_click(self, server_client, local_client, button):
        """
        版本更新触发函数
        """
        app_exec = None
        server_ver = '0'
        local_ver = '0'
        if server_client:
            server_ver = server_client.get('version')
        if local_client:
            app_exec = os.path.basename(local_client['app_path'])
            local_ver = local_client.get('version')

        if not server_client or cmp_version(server_ver, local_ver):
            import subprocess
            print local_client['app_path']
            subprocess.Popen(local_client['app_path'])  # 非阻塞
        else:
            button.setEnabled(False)
            if checkhct(app_exec):
                self.upgrade_prompt(button, app_exec, server_client)
            else:
                self.upgrade_dialog(server_client, button)

    def upgrade_prompt(self, button, app_exec, server_client):
        """
        当发现进程已经启动时，提示用户杀死进程，根据用户对提示的操作进行相应的业务流程
        :param button: 点击的按钮
        :param app_exec: 该客户端的进程名
        :param server_client: 服务端的该app信息
        :return:
        """
        if self.prompt(app_exec):
            self.upgrade_dialog(server_client, button)
        else:
            button.setEnabled(True)

    def prompt(self, app_exec):
        """
        检测该进程已经启动，提示是否杀死，杀死返回True，反之返回False
        """
        flag = False
        reply = QMessageBox.question(self, 'Message', u'该程序处于启动中，是否终止？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            command = 'taskkill /F /IM %s' % app_exec  # 杀死所点击的客户端进程
            os.system(command)
            flag = True

        return flag

    def upgrade_dialog(self, server_client, button):
        """
        启动升级对话框
        """
        self.dialog.startDialog.emit(server_client)
        result = self.dialog.exec_()
        if not result:
            button.setEnabled(True)

    def repair_dialog(self, local_client):
        """
        启动修复对话框
        """
        dialog = QDialog()
        dialog.setWindowTitle("Repair")
        dialog.resize(150, 100)
        layout = QtGui.QVBoxLayout()
        label = QtGui.QLabel(u'%s 修复成功' % local_client['app_id'], dialog)
        layout.addWidget(label)

        verify_button = QtGui.QPushButton(u'OK')
        verify_button.clicked.connect(dialog.close)
        layout.addWidget(verify_button)
        dialog.setLayout(layout)
        dialog.exec_()

    def finish_upgrade(self):
        """
        完成升级后重新检测服务和本地客户端版本
        """
        self.detection.start()
