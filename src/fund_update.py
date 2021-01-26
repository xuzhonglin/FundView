#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time     : 2021/1/26 15:59
@Author   : colinxu
@File     : fund_update.py
@Desc     : 
"""
import _thread
import os

import requests
from PyQt5.QtCore import pyqtSignal, Qt, QObject
from PyQt5.QtWidgets import QDialog
from tqdm import tqdm

from fundConfig import FundConfig
from fundUtils import compare_version
from fund_update_dialog import Ui_FundUpdateDialog


class FundUpdate(QObject):
    process_signal = pyqtSignal(int)
    download_done_signal = pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.args = []
        self.update_filename = ''

    def update(self, args):
        self.args = args
        resp = requests.get(FundConfig.UPDATE_URL)
        if resp.status_code == 200:
            resp_json = resp.json()
            latest_version = resp_json['latestVersion']
            force_update = resp_json['forceUpdate']
            chang_log = resp_json['changeLog']
            publish_time = resp_json['publishTime']
            update_info = '当前版本：{}，最新版本：{}，发布日期：{}'.format(FundConfig.VERSION, latest_version, publish_time)
            # 有新版本
            if compare_version(FundConfig.VERSION, latest_version):
                title = '更新提醒'
                dialog = QDialog(self.parent.centralwidget)
                update_ui = Ui_FundUpdateDialog()
                update_ui.setupUi(dialog)
                update_ui.update_process_bar.hide()
                update_ui.version_info_txt.setText(update_info)
                update_ui.chang_log_brower.append(chang_log)
                if force_update:
                    update_ui.update_now_btn.hide()
                    update_ui.next_time_btn.setText('立即更新')
                    # 隐藏关闭按钮
                    dialog.setWindowFlags(Qt.Window | Qt.WindowTitleHint)
                if not force_update:
                    update_ui.update_now_btn.clicked.connect(lambda: self.dl_update(update_ui, resp_json))
                    update_ui.next_time_btn.clicked.connect(lambda: dialog.accept())
                else:
                    update_ui.next_time_btn.clicked.connect(lambda: self.dl_update(update_ui, resp_json))
                self.process_signal.connect(lambda x: update_ui.update_process_bar.setValue(x))
                self.download_done_signal.connect(lambda: self.complete_update(update_ui))
                dialog.setWindowTitle(title)
                dialog.exec_()
            else:
                print('暂无更新')

    def dl_update(self, dialog: Ui_FundUpdateDialog, update_info: dict):
        dialog.update_now_btn.setEnabled(False)
        dialog.next_time_btn.setEnabled(False)
        dialog.update_process_bar.setValue(0)
        dialog.update_process_bar.show()
        dl_url = update_info['fileUrl-win32'] if FundConfig.PLATFORM == 'win32' else update_info['fileUrl-darwin']
        filepath, filename = os.path.split(os.path.abspath(self.args[0]))
        file_ext = 'exe' if FundConfig.PLATFORM == 'win32' else 'app'
        self.update_filename = filepath + '/' + FundConfig.APP_NAME + '-' + update_info[
            'latestVersion'] + '.' + file_ext
        _thread.start_new_thread(self.download_from_url, (dl_url, self.update_filename,))

    def complete_update(self, dialog):
        dialog.update_process_bar.hide()
        # exit(0)
        self.parent.hide()
        os.system(self.update_filename)
        exit(0)

    def download_from_url(self, url, dst):
        """
        @param: url to download file
        @param: dst place to put the file
        """
        file_size = int(requests.get(url, stream=True).headers['Content-Length'])
        # if os.path.exists(dst):
        #     first_byte = os.path.getsize(dst)
        # else:
        #     first_byte = 0
        # if first_byte >= file_size:
        #     return file_size
        first_byte = 0

        header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
        pbar = tqdm(
            total=file_size, initial=first_byte,
            unit='B', unit_scale=True, desc=url.split('/')[-1])
        req = requests.get(url, headers=header, stream=True)
        chunk_size = 1024
        times = file_size // chunk_size
        process_value = 0
        with(open(dst, 'ab')) as f:
            for chunk in req.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    process_value = process_value + (1 / times) * 100
                    self.process_signal.emit(int(process_value))
                    pbar.update(1024)
        self.download_done_signal.emit()
        pbar.close()
        return file_size
